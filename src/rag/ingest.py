from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import chromadb
import requests
from pypdf import PdfReader


RAW_DIR = Path("data/raw")
CHROMA_DIR = Path("data/chroma")

COLLECTION_NAME = "university_books"
EMBEDDING_MODEL = "embeddinggemma"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200
BATCH_SIZE = 16


def clean_text(text: str) -> str:
    """Limpa espaços excessivos do texto extraído."""
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def split_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    """Divide o texto em chunks com sobreposição."""
    if chunk_size <= 0:
        raise ValueError("chunk_size deve ser maior que zero.")

    if overlap < 0:
        raise ValueError("overlap não pode ser negativo.")

    if overlap >= chunk_size:
        raise ValueError("overlap deve ser menor que chunk_size.")

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


def extract_pdf(pdf_path: Path) -> list[dict[str, Any]]:
    """Extrai texto de um PDF mantendo página e índice do chunk."""
    reader = PdfReader(pdf_path)
    records: list[dict[str, Any]] = []

    total_pages = len(reader.pages)

    print(f"  Páginas: {total_pages}")

    for page_number, page in enumerate(reader.pages, start=1):
        raw_text = page.extract_text() or ""
        text = clean_text(raw_text)

        if not text:
            continue

        page_chunks = split_text(text)

        for chunk_index, chunk in enumerate(page_chunks):
            records.append(
                {
                    "document": chunk,
                    "metadata": {
                        "source": pdf_path.name,
                        "page": page_number,
                        "chunk_index": chunk_index,
                    },
                }
            )

        if page_number % 100 == 0 or page_number == total_pages:
            print(f"  Extração: {page_number}/{total_pages} páginas")

    return records


def create_id(
    source: str,
    page: int,
    chunk_index: int,
) -> str:
    """Cria um identificador determinístico para cada chunk."""
    raw_id = f"{source}:{page}:{chunk_index}"
    return hashlib.sha256(raw_id.encode("utf-8")).hexdigest()


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Gera embeddings localmente por meio do Ollama."""
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": EMBEDDING_MODEL,
            "input": texts,
        },
        timeout=600,
    )

    response.raise_for_status()

    data = response.json()
    embeddings = data.get("embeddings")

    if not embeddings:
        raise RuntimeError("O Ollama não retornou embeddings.")

    if len(embeddings) != len(texts):
        raise RuntimeError(
            "A quantidade de embeddings retornada "
            "não corresponde à quantidade de textos."
        )

    return embeddings


def check_ollama() -> None:
    """Verifica se o Ollama e o modelo de embeddings estão acessíveis."""
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(
            "Não foi possível acessar o Ollama. Execute:\nsudo systemctl start ollama"
        ) from exc

    model_names = {model["name"] for model in response.json().get("models", [])}

    if not any(name.startswith(EMBEDDING_MODEL) for name in model_names):
        raise RuntimeError(
            f"O modelo {EMBEDDING_MODEL!r} não está instalado. "
            f"Execute:\nollama pull {EMBEDDING_MODEL}"
        )


def main() -> None:
    print()
    print("Iniciando ingestão do RAG")
    print(f"Pasta de PDFs: {RAW_DIR.resolve()}")
    print(f"Banco vetorial: {CHROMA_DIR.resolve()}")
    print()

    check_ollama()

    pdf_files = sorted(RAW_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"Nenhum PDF encontrado em {RAW_DIR.resolve()}.")

    print(f"PDFs encontrados: {len(pdf_files)}")

    for pdf_path in pdf_files:
        print(f"  - {pdf_path.name}")

    print()

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    all_records: list[dict[str, Any]] = []

    for pdf_path in pdf_files:
        print(f"Extraindo: {pdf_path.name}")

        records = extract_pdf(pdf_path)

        print(f"  Chunks extraídos: {len(records)}")
        print()

        all_records.extend(records)

    if not all_records:
        raise RuntimeError("Nenhum texto foi extraído dos PDFs.")

    total_records = len(all_records)

    print(f"Total de chunks: {total_records}")
    print("Gerando embeddings e indexando...")
    print()

    for batch_start in range(
        0,
        total_records,
        BATCH_SIZE,
    ):
        batch = all_records[batch_start : batch_start + BATCH_SIZE]

        documents = [record["document"] for record in batch]

        metadatas = [record["metadata"] for record in batch]

        ids = [
            create_id(
                source=str(metadata["source"]),
                page=int(metadata["page"]),
                chunk_index=int(metadata["chunk_index"]),
            )
            for metadata in metadatas
        ]

        embeddings = embed_texts(documents)

        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

        processed = min(
            batch_start + len(batch),
            total_records,
        )

        print(f"Indexados: {processed}/{total_records}")

    print()
    print("Ingestão concluída com sucesso.")
    print(f"Chunks armazenados: {collection.count()}")
    print(f"Coleção: {COLLECTION_NAME}")
    print(f"Banco salvo em: {CHROMA_DIR.resolve()}")


if __name__ == "__main__":
    main()
