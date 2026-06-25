from __future__ import annotations

import json
import re
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Tag


SOURCES_FILE = Path("data/sources.json")
RAW_DATA_DIR = Path("data/raw")

REQUEST_TIMEOUT = 60
REQUEST_DELAY_SECONDS = 1.0

USER_AGENT = "PrivateQwenTrainingCorpusCollector/0.1 (educational local RAG project)"


@dataclass(frozen=True)
class Source:
    id: str
    domain: str
    topic: str
    title: str
    source_type: str
    url: str
    license: str
    language: str
    enabled: bool


@dataclass(frozen=True)
class CollectedDocument:
    source_id: str
    domain: str
    topic: str
    title: str
    url: str
    license: str
    language: str
    source_type: str
    hostname: str
    collected_at: str
    content_file: str
    character_count: int
    word_count: int


def load_sources() -> list[Source]:
    if not SOURCES_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo de fontes não encontrado: {SOURCES_FILE.resolve()}"
        )

    payload = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    raw_sources = payload.get("sources")

    if not isinstance(raw_sources, list):
        raise ValueError(
            "O arquivo data/sources.json deve conter uma lista em 'sources'."
        )

    sources: list[Source] = []

    for index, raw_source in enumerate(raw_sources):
        if not isinstance(raw_source, dict):
            raise ValueError(f"A fonte de índice {index} não é um objeto JSON.")

        try:
            source = Source(
                id=str(raw_source["id"]),
                domain=str(raw_source["domain"]),
                topic=str(raw_source["topic"]),
                title=str(raw_source["title"]),
                source_type=str(raw_source["source_type"]),
                url=str(raw_source["url"]),
                license=str(raw_source["license"]),
                language=str(raw_source["language"]),
                enabled=bool(raw_source.get("enabled", True)),
            )
        except KeyError as exc:
            raise ValueError(
                f"Campo obrigatório ausente na fonte {index}: {exc}"
            ) from exc

        sources.append(source)

    return sources


def validate_source(source: Source) -> None:
    parsed = urlparse(source.url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"URL inválida para {source.id}: {source.url}")

    if not parsed.netloc:
        raise ValueError(f"A URL da fonte {source.id} não possui domínio.")

    if not re.fullmatch(r"[a-zA-Z0-9_-]+", source.id):
        raise ValueError(
            f"ID inválido: {source.id!r}. Use letras, números, hífen ou underscore."
        )

    if not re.fullmatch(r"[a-zA-Z0-9_-]+", source.domain):
        raise ValueError(f"Domínio inválido: {source.domain!r}.")


def download_html(
    session: requests.Session,
    source: Source,
) -> str:
    response = session.get(
        source.url,
        timeout=REQUEST_TIMEOUT,
        allow_redirects=True,
    )
    response.raise_for_status()

    content_type = response.headers.get(
        "content-type",
        "",
    ).lower()

    if "text/html" not in content_type:
        raise ValueError(
            f"A fonte {source.id} não retornou HTML. "
            f"Content-Type recebido: "
            f"{content_type or 'desconhecido'}"
        )

    return response.text


def remove_irrelevant_elements(
    soup: BeautifulSoup,
) -> None:
    selectors = [
        "script",
        "style",
        "noscript",
        "svg",
        "canvas",
        "iframe",
        "nav",
        "footer",
        "header",
        "form",
        "button",
        "[role='navigation']",
        "[role='banner']",
        "[role='contentinfo']",
        ".sidebar",
        ".sphinxsidebar",
        ".wy-nav-side",
        ".wy-side-nav-search",
        ".toc",
        ".table-of-contents",
        ".breadcrumbs",
        ".breadcrumb",
        ".pagination",
        ".prev-next-area",
        ".related",
        ".footer",
        ".header",
        ".navbar",
        ".announcement",
    ]

    for selector in selectors:
        for element in soup.select(selector):
            element.decompose()


def select_main_content(
    soup: BeautifulSoup,
) -> Tag:
    selectors = [
        "main",
        "article",
        "[role='main']",
        ".document",
        ".body",
        ".content",
        ".main-content",
        "#main-content",
        "#content",
    ]

    for selector in selectors:
        element = soup.select_one(selector)

        if isinstance(element, Tag):
            return element

    if soup.body is not None:
        return soup.body

    return soup


def normalize_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    lines = [line.strip() for line in text.splitlines()]

    cleaned_lines = [line for line in lines if line]

    return "\n\n".join(cleaned_lines).strip()


def clean_title(title: str) -> str:
    """Remove marcadores residuais do título."""
    return re.sub(
        r"\s*#+\s*$",
        "",
        title,
    ).strip()


def is_noise_block(text: str) -> bool:
    """Identifica navegação e downloads inúteis ao RAG."""
    normalized = text.casefold().strip()

    noise_prefixes = (
        "download jupyter notebook",
        "download python source code",
        "download zipped",
        "previous",
        "next",
        "edit this page",
        "view page source",
        "table of contents",
    )

    return normalized.startswith(noise_prefixes)


def deduplicate_blocks(
    blocks: list[str],
) -> list[str]:
    """Remove blocos duplicados, incluindo variações de Markdown."""
    unique_blocks: list[str] = []
    seen: set[str] = set()

    for block in blocks:
        comparison_text = block.strip()

        # Remove marcadores Markdown usados apenas para apresentação.
        comparison_text = re.sub(
            r"^(?:[-*+]\s+|>\s+|#{1,6}\s+)",
            "",
            comparison_text,
        )

        # Remove crases usadas em código inline.
        comparison_text = comparison_text.strip("`")

        normalized = (
            re.sub(
                r"\s+",
                " ",
                comparison_text,
            )
            .casefold()
            .strip()
        )

        if not normalized:
            continue

        if normalized in seen:
            continue

        if is_noise_block(comparison_text):
            continue

        seen.add(normalized)
        unique_blocks.append(block)

    return unique_blocks


def html_to_markdown_like_text(
    html: str,
    fallback_title: str,
) -> tuple[str, str]:
    soup = BeautifulSoup(html, "lxml")

    remove_irrelevant_elements(soup)
    main_content = select_main_content(soup)

    page_title = clean_title(fallback_title)

    heading = main_content.find(["h1", "h2"])

    if isinstance(heading, Tag):
        heading_text = heading.get_text(
            " ",
            strip=True,
        )

        if heading_text:
            page_title = clean_title(heading_text)

    blocks: list[str] = []

    for element in main_content.find_all(
        [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "li",
            "pre",
            "code",
            "blockquote",
            "dt",
            "dd",
        ]
    ):
        if not isinstance(element, Tag):
            continue

        if (
            element.name == "code"
            and element.parent is not None
            and element.parent.name == "pre"
        ):
            continue

        text = element.get_text(
            " ",
            strip=True,
        )

        if not text:
            continue

        if element.name in {
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
        }:
            level = int(element.name[1])
            clean_heading = clean_title(text)
            blocks.append(f"{'#' * level} {clean_heading}")
            continue

        if element.name == "li":
            blocks.append(f"- {text}")
            continue

        if element.name == "pre":
            code_text = element.get_text(
                "\n",
                strip=True,
            )
            blocks.append(f"```\n{code_text}\n```")
            continue

        if element.name == "code":
            blocks.append(f"`{text}`")
            continue

        if element.name == "blockquote":
            blocks.append(f"> {text}")
            continue

        blocks.append(text)

    blocks = deduplicate_blocks(blocks)

    content = normalize_text("\n\n".join(blocks))

    return page_title, content


def save_document(
    source: Source,
    title: str,
    content: str,
) -> CollectedDocument:
    domain_dir = RAW_DATA_DIR / source.domain
    domain_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    content_path = domain_dir / f"{source.id}.md"

    metadata_path = domain_dir / f"{source.id}.metadata.json"

    markdown_header = "\n".join(
        [
            "---",
            f"source_id: {source.id}",
            (f"title: {json.dumps(title, ensure_ascii=False)}"),
            f"domain: {source.domain}",
            f"topic: {source.topic}",
            f"url: {source.url}",
            f"license: {source.license}",
            f"language: {source.language}",
            f"source_type: {source.source_type}",
            "---",
            "",
        ]
    )

    content_path.write_text(
        markdown_header + content + "\n",
        encoding="utf-8",
    )

    word_count = len(content.split())

    document = CollectedDocument(
        source_id=source.id,
        domain=source.domain,
        topic=source.topic,
        title=title,
        url=source.url,
        license=source.license,
        language=source.language,
        source_type=source.source_type,
        hostname=urlparse(source.url).netloc,
        collected_at=datetime.now(UTC).isoformat(),
        content_file=str(content_path),
        character_count=len(content),
        word_count=word_count,
    )

    metadata_path.write_text(
        json.dumps(
            asdict(document),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    return document


def collect_source(
    session: requests.Session,
    source: Source,
) -> CollectedDocument:
    validate_source(source)

    print(f"Coletando: {source.id}")
    print(f"  URL: {source.url}")

    html = download_html(
        session=session,
        source=source,
    )

    title, content = html_to_markdown_like_text(
        html=html,
        fallback_title=source.title,
    )

    if len(content) < 200:
        raise RuntimeError(
            f"Pouco conteúdo foi extraído "
            f"da fonte {source.id}: "
            f"{len(content)} caracteres."
        )

    document = save_document(
        source=source,
        title=title,
        content=content,
    )

    print(f"  Título: {document.title}")
    print(f"  Caracteres: {document.character_count}")
    print(f"  Palavras: {document.word_count}")
    print(f"  Arquivo: {document.content_file}")

    return document


def main() -> None:
    sources = load_sources()

    enabled_sources = [source for source in sources if source.enabled]

    if not enabled_sources:
        raise RuntimeError("Nenhuma fonte habilitada em data/sources.json.")

    print()
    print("Coletor de corpus técnico")
    print(f"Fontes habilitadas: {len(enabled_sources)}")
    print()

    session = requests.Session()

    session.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
            ),
        }
    )

    collected: list[CollectedDocument] = []
    failures: list[dict[str, Any]] = []

    for index, source in enumerate(
        enabled_sources,
        start=1,
    ):
        print(f"[{index}/{len(enabled_sources)}] {source.title}")

        try:
            document = collect_source(
                session=session,
                source=source,
            )
            collected.append(document)

        except Exception as exc:
            failures.append(
                {
                    "source_id": source.id,
                    "url": source.url,
                    "error": str(exc),
                }
            )

            print(f"  ERRO: {exc}")

        print()

        if index < len(enabled_sources):
            time.sleep(REQUEST_DELAY_SECONDS)

    report_path = RAW_DATA_DIR / "collection_report.json"

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "sources_requested": len(enabled_sources),
        "sources_collected": len(collected),
        "sources_failed": len(failures),
        "documents": [asdict(document) for document in collected],
        "failures": failures,
    }

    report_path.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print("Coleta concluída.")
    print(f"Sucessos: {len(collected)}")
    print(f"Falhas: {len(failures)}")
    print(f"Relatório: {report_path.resolve()}")

    if failures:
        print()
        print("Fontes com falha:")

        for failure in failures:
            print(f"  - {failure['source_id']}: {failure['error']}")


if __name__ == "__main__":
    main()
