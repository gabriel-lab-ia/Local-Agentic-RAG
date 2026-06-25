from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb
import requests
from chromadb.api.models.Collection import Collection


RAW_DATA_DIR = Path("data/raw")
CHROMA_DIR = Path("data/chroma")

COLLECTION_NAME = "ai_engineering_knowledge"

OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "embeddinggemma"

SUPPORTED_DOMAINS = {
    "python",
    "pytorch",
    "machine_learning",
    "deep_learning",
    "reinforcement_learning",
    "mlops",
    "llmops",
    "agentic_ai",
}

CHUNK_SIZE = 1400
CHUNK_OVERLAP = 220
EMBEDDING_BATCH_SIZE = 16
REQUEST_TIMEOUT = 120


@dataclass(frozen=True)
class TechnicalDocument:
    path: Path
    content: str
    metadata: dict[str, str]


@dataclass(frozen=True)
class TechnicalChunk:
    chunk_id: str
    text: str
    metadata: dict[str, str | int]


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Extrai o front matter simples delimitado por linhas com ---."""
    if not text.startswith("---"):
        return {}, text.strip()

    parts = text.split("---", maxsplit=2)

    if len(parts) < 3:
        return {}, text.strip()

    raw_metadata = parts[1]
    content = parts[2].strip()

    metadata: dict[str, str] = {}

    for line in raw_metadata.splitlines():
        line = line.strip()

        if not line or ":" not in line:
            continue

        key, value = line.split(":", maxsplit=1)
        key = key.strip()
        value = value.strip()

        if value.startswith('"') and value.endswith('"'):
            try:
                value = str(json.loads(value))
            except json.JSONDecodeError:
                value = value.strip('"')

        metadata[key] = value

    return metadata, content


def discover_markdown_files() -> list[Path]:
    """Localiza documentos Markdown dos domínios técnicos permitidos."""
    files: list[Path] = []

    for domain in sorted(SUPPORTED_DOMAINS):
        domain_dir = RAW_DATA_DIR / domain

        if not domain_dir.exists():
            continue

        files.extend(sorted(domain_dir.rglob("*.md")))

    return files


def load_document(path: Path) -> TechnicalDocument:
    text = path.read_text(encoding="utf-8")
    metadata, content = parse_front_matter(text)

    if not content.strip():
        raise ValueError(f"Documento vazio: {path}")

    relative_path = path.relative_to(RAW_DATA_DIR)
    domain = relative_path.parts[0]

    default_source_id = "_".join(relative_path.with_suffix("").parts)

    metadata.setdefault("source_id", default_source_id)
    metadata.setdefault("title", path.stem.replace("_", " ").title())
    metadata.setdefault("domain", domain)
    metadata.setdefault("topic", "general")
    metadata.setdefault("url", "")
    metadata.setdefault("license", "unknown")
    metadata.setdefault("language", "en")
    metadata.setdefault("source_type", "technical_documentation")

    metadata["source_path"] = str(path)

    return TechnicalDocument(
        path=path,
        content=content,
        metadata=metadata,
    )


def split_markdown_sections(content: str) -> list[tuple[str, str]]:
    """
    Divide o Markdown por títulos.

    Cada seção retorna:
    (título_da_seção, conteúdo_da_seção)
    """
    sections: list[tuple[str, str]] = []

    current_heading = "Document"
    current_lines: list[str] = []

    heading_pattern = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

    for line in content.splitlines():
        heading_match = heading_pattern.match(line)

        if heading_match:
            section_text = "\n".join(current_lines).strip()

            if section_text:
                sections.append(
                    (
                        current_heading,
                        section_text,
                    )
                )

            current_heading = heading_match.group(2).strip()
            current_lines = []
            continue

        current_lines.append(line)

    final_text = "\n".join(current_lines).strip()

    if final_text:
        sections.append(
            (
                current_heading,
                final_text,
            )
        )

    if not sections and content.strip():
        sections.append(
            (
                "Document",
                content.strip(),
            )
        )

    return sections


def split_long_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """Divide texto longo preservando parágrafos quando possível."""
    text = text.strip()

    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    paragraphs = [
        paragraph.strip()
        for paragraph in re.split(r"\n\s*\n", text)
        if paragraph.strip()
    ]

    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip() if current else paragraph

        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            chunks.append(current)

        if len(paragraph) <= chunk_size:
            current = paragraph
            continue

        start = 0

        while start < len(paragraph):
            end = min(
                start + chunk_size,
                len(paragraph),
            )

            chunk = paragraph[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(paragraph):
                break

            start = max(
                end - overlap,
                start + 1,
            )

        current = ""

    if current:
        chunks.append(current)

    return chunks


def build_chunks(
    document: TechnicalDocument,
) -> list[TechnicalChunk]:
    chunks: list[TechnicalChunk] = []

    sections = split_markdown_sections(document.content)

    chunk_index = 0

    for section_index, (
        section_title,
        section_content,
    ) in enumerate(sections):
        section_text = (
            f"Title: {document.metadata['title']}\n"
            f"Section: {section_title}\n\n"
            f"{section_content}"
        )

        section_chunks = split_long_text(section_text)

        for section_chunk_index, chunk_text in enumerate(section_chunks):
            identity = (
                f"{document.metadata['source_id']}|"
                f"{section_index}|"
                f"{section_chunk_index}|"
                f"{chunk_text}"
            )

            digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:20]

            chunk_id = f"{document.metadata['source_id']}-{digest}"

            metadata: dict[str, str | int] = {
                **document.metadata,
                "section": section_title,
                "section_index": section_index,
                "chunk_index": chunk_index,
                "character_count": len(chunk_text),
            }

            chunks.append(
                TechnicalChunk(
                    chunk_id=chunk_id,
                    text=chunk_text,
                    metadata=metadata,
                )
            )

            chunk_index += 1

    return chunks


def embed_batch(
    texts: list[str],
) -> list[list[float]]:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embed",
        json={
            "model": EMBEDDING_MODEL,
            "input": texts,
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    payload = response.json()
    embeddings = payload.get("embeddings")

    if not isinstance(embeddings, list):
        raise RuntimeError("Ollama não retornou a lista 'embeddings'.")

    if len(embeddings) != len(texts):
        raise RuntimeError(
            "Quantidade de embeddings diferente da quantidade de textos enviados."
        )

    return embeddings


def create_collection(
    client: chromadb.PersistentClient,
    rebuild: bool,
) -> Collection:
    if rebuild:
        try:
            client.delete_collection(COLLECTION_NAME)
            print(f"Coleção anterior removida: {COLLECTION_NAME}")
        except Exception:
            pass

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description": ("Official technical documentation for AI engineering"),
            "embedding_model": EMBEDDING_MODEL,
            "hnsw:space": "cosine",
        },
    )


def upsert_chunks(
    collection: Collection,
    chunks: list[TechnicalChunk],
) -> None:
    total = len(chunks)

    for batch_start in range(
        0,
        total,
        EMBEDDING_BATCH_SIZE,
    ):
        batch = chunks[batch_start : batch_start + EMBEDDING_BATCH_SIZE]

        texts = [chunk.text for chunk in batch]

        embeddings = embed_batch(texts)

        collection.upsert(
            ids=[chunk.chunk_id for chunk in batch],
            documents=texts,
            embeddings=embeddings,
            metadatas=[chunk.metadata for chunk in batch],
        )

        completed = min(
            batch_start + len(batch),
            total,
        )

        print(f"  Embeddings indexados: {completed}/{total}")


def build_ingestion_report(
    documents: list[TechnicalDocument],
    chunks: list[TechnicalChunk],
    collection_count: int,
) -> dict[str, Any]:
    domain_counts: dict[str, int] = {}
    source_counts: dict[str, int] = {}

    for chunk in chunks:
        domain = str(chunk.metadata["domain"])
        source_id = str(chunk.metadata["source_id"])

        domain_counts[domain] = domain_counts.get(domain, 0) + 1

        source_counts[source_id] = source_counts.get(source_id, 0) + 1

    return {
        "collection": COLLECTION_NAME,
        "embedding_model": EMBEDDING_MODEL,
        "documents_processed": len(documents),
        "chunks_generated": len(chunks),
        "collection_count": collection_count,
        "chunk_size": CHUNK_SIZE,
        "chunk_overlap": CHUNK_OVERLAP,
        "domains": domain_counts,
        "sources": source_counts,
        "documents": [
            {
                "path": str(document.path),
                "source_id": (document.metadata["source_id"]),
                "title": document.metadata["title"],
                "domain": document.metadata["domain"],
                "topic": document.metadata["topic"],
                "url": document.metadata["url"],
                "license": (document.metadata["license"]),
            }
            for document in documents
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=("Indexa documentação técnica em uma coleção Chroma separada.")
    )

    parser.add_argument(
        "--rebuild",
        action="store_true",
        help=("Remove e recria a coleção antes da ingestão."),
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    markdown_files = discover_markdown_files()

    if not markdown_files:
        raise RuntimeError(
            "Nenhum arquivo Markdown técnico foi encontrado em data/raw/."
        )

    print()
    print("Ingestão de corpus técnico")
    print(f"Arquivos encontrados: {len(markdown_files)}")
    print(f"Coleção: {COLLECTION_NAME}")
    print(f"Embedding: {EMBEDDING_MODEL}")
    print()

    documents: list[TechnicalDocument] = []
    chunks: list[TechnicalChunk] = []

    for path in markdown_files:
        print(f"Lendo: {path}")

        document = load_document(path)
        document_chunks = build_chunks(document)

        documents.append(document)
        chunks.extend(document_chunks)

        print(f"  Fonte: {document.metadata['source_id']}")
        print(f"  Domínio: {document.metadata['domain']}")
        print(f"  Chunks: {len(document_chunks)}")

    print()
    print(f"Total de chunks: {len(chunks)}")
    print()

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = create_collection(
        client=client,
        rebuild=args.rebuild,
    )

    upsert_chunks(
        collection=collection,
        chunks=chunks,
    )

    collection_count = collection.count()

    report = build_ingestion_report(
        documents=documents,
        chunks=chunks,
        collection_count=collection_count,
    )

    report_path = Path("data/processed") / "technical_ingestion_report.json"

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path.write_text(
        json.dumps(
            report,
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print("Ingestão concluída.")
    print(f"Documentos processados: {len(documents)}")
    print(f"Chunks gerados nesta execução: {len(chunks)}")
    print(f"Chunks presentes na coleção: {collection_count}")
    print(f"Relatório: {report_path.resolve()}")


if __name__ == "__main__":
    main()
