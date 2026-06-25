from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb
import requests
from chromadb.api.models.Collection import Collection


CHROMA_DIR = Path("data/chroma")
COLLECTION_NAME = "ai_engineering_knowledge"

OLLAMA_BASE_URL = "http://localhost:11434"
CHAT_MODEL = "qwen3:4b"
EMBEDDING_MODEL = "embeddinggemma"

DEFAULT_TOP_K = 5
REQUEST_TIMEOUT = 180


@dataclass(frozen=True)
class RetrievedChunk:
    document: str
    metadata: dict[str, Any]
    distance: float


def embed_query(query: str) -> list[float]:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/embed",
        json={
            "model": EMBEDDING_MODEL,
            "input": query,
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    payload = response.json()
    embeddings = payload.get("embeddings")

    if not isinstance(embeddings, list) or not embeddings:
        raise RuntimeError("Ollama não retornou embeddings para a pergunta.")

    embedding = embeddings[0]

    if not isinstance(embedding, list):
        raise RuntimeError("O embedding retornado possui formato inválido.")

    return embedding


def get_collection() -> Collection:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    try:
        return client.get_collection(COLLECTION_NAME)
    except Exception as exc:
        raise RuntimeError(
            f"A coleção {COLLECTION_NAME!r} "
            "não foi encontrada. Execute primeiro:\n"
            "uv run python -m "
            "src.rag.ingest_technical --rebuild"
        ) from exc


def retrieve_chunks(
    collection: Collection,
    query: str,
    top_k: int,
    domain: str | None = None,
) -> list[RetrievedChunk]:
    query_embedding = embed_query(query)

    where = None

    if domain:
        where = {
            "domain": domain,
        }

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where=where,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = results.get("documents")
    metadatas = results.get("metadatas")
    distances = results.get("distances")

    if not documents or not documents[0]:
        return []

    first_documents = documents[0]
    first_metadatas = metadatas[0] if metadatas else []
    first_distances = distances[0] if distances else []

    chunks: list[RetrievedChunk] = []

    for index, document in enumerate(first_documents):
        metadata: dict[str, Any] = {}

        if index < len(first_metadatas):
            raw_metadata = first_metadatas[index]

            if isinstance(raw_metadata, dict):
                metadata = raw_metadata

        distance = 0.0

        if index < len(first_distances):
            raw_distance = first_distances[index]

            if isinstance(raw_distance, int | float):
                distance = float(raw_distance)

        chunks.append(
            RetrievedChunk(
                document=str(document),
                metadata=metadata,
                distance=distance,
            )
        )

    return chunks


def format_context(
    chunks: list[RetrievedChunk],
) -> str:
    context_blocks: list[str] = []

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):
        metadata = chunk.metadata

        title = metadata.get(
            "title",
            "Unknown title",
        )
        section = metadata.get(
            "section",
            "Unknown section",
        )
        domain = metadata.get(
            "domain",
            "unknown",
        )
        topic = metadata.get(
            "topic",
            "unknown",
        )
        url = metadata.get(
            "url",
            "",
        )

        context_blocks.append(
            "\n".join(
                [
                    f"[Fonte {index}]",
                    f"Título: {title}",
                    f"Seção: {section}",
                    f"Domínio: {domain}",
                    f"Tópico: {topic}",
                    f"URL: {url}",
                    (f"Distância vetorial: {chunk.distance:.4f}"),
                    "",
                    chunk.document,
                ]
            )
        )

    return "\n\n---\n\n".join(context_blocks)


def build_system_prompt() -> str:
    return """
Você é um assistente técnico especializado em engenharia de
inteligência artificial, PyTorch e reinforcement learning.

Responda usando prioritariamente o contexto recuperado da
documentação oficial.

Regras:
1. Não invente informações ausentes no contexto.
2. Diferencie claramente fatos documentados de inferências.
3. Cite as fontes no formato [Fonte 1], [Fonte 2].
4. Seja tecnicamente preciso e explique os conceitos.
5. Preserve nomes de classes, funções, APIs e algoritmos.
6. Quando o contexto for insuficiente, diga explicitamente.
7. Não trate distância vetorial como probabilidade.
8. Quando houver código no contexto, explique sua finalidade.
9. Responda em português, mantendo termos técnicos em inglês
   quando isso for convencional.
""".strip()


def ask_qwen(
    question: str,
    context: str,
) -> str:
    user_prompt = f"""
CONTEXTO RECUPERADO:

{context}

PERGUNTA:

{question}

Produza uma resposta técnica fundamentada no contexto e cite
as fontes utilizadas.
""".strip()

    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": CHAT_MODEL,
            "stream": False,
            "messages": [
                {
                    "role": "system",
                    "content": build_system_prompt(),
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "options": {
                "temperature": 0.2,
                "num_ctx": 8192,
            },
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    payload = response.json()
    message = payload.get("message")

    if not isinstance(message, dict):
        raise RuntimeError("Ollama não retornou uma mensagem válida.")

    content = message.get("content")

    if not isinstance(content, str):
        raise RuntimeError("Ollama não retornou conteúdo textual.")

    return content.strip()


def print_sources(
    chunks: list[RetrievedChunk],
) -> None:
    print()
    print("Fontes recuperadas:")

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):
        metadata = chunk.metadata

        title = metadata.get(
            "title",
            "Unknown title",
        )
        section = metadata.get(
            "section",
            "Unknown section",
        )
        domain = metadata.get(
            "domain",
            "unknown",
        )
        url = metadata.get(
            "url",
            "",
        )

        print(f"[{index}] {title} — {section}")
        print(f"    domínio: {domain}")
        print(f"    distância: {chunk.distance:.4f}")

        if url:
            print(f"    URL: {url}")


def answer_question(
    collection: Collection,
    question: str,
    top_k: int,
    domain: str | None,
) -> None:
    chunks = retrieve_chunks(
        collection=collection,
        query=question,
        top_k=top_k,
        domain=domain,
    )

    if not chunks:
        print("Nenhum trecho técnico relevante foi encontrado.")
        return

    context = format_context(chunks)

    answer = ask_qwen(
        question=question,
        context=context,
    )

    print()
    print("Resposta:")
    print()
    print(answer)

    print_sources(chunks)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Chat técnico com RAG sobre documentação oficial de engenharia de IA."
        )
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=(f"Número de chunks recuperados (padrão: {DEFAULT_TOP_K})."),
    )

    parser.add_argument(
        "--domain",
        type=str,
        default=None,
        help=(
            "Filtra a busca por domínio, como 'pytorch' ou 'reinforcement_learning'."
        ),
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.top_k < 1:
        raise ValueError("--top-k deve ser maior que zero.")

    collection = get_collection()

    print()
    print("Technical AI Engineering RAG")
    print(f"Modelo: {CHAT_MODEL}")
    print(f"Embedding: {EMBEDDING_MODEL}")
    print(f"Coleção: {COLLECTION_NAME}")
    print(f"Chunks disponíveis: {collection.count()}")

    if args.domain:
        print(f"Filtro de domínio: {args.domain}")

    print()
    print("Digite uma pergunta técnica ou 'sair'.")

    while True:
        try:
            question = input("\nVocê: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando.")
            break

        if question.casefold() in {
            "sair",
            "exit",
            "quit",
        }:
            print("Encerrando.")
            break

        if not question:
            print("Digite uma pergunta não vazia.")
            continue

        try:
            answer_question(
                collection=collection,
                question=question,
                top_k=args.top_k,
                domain=args.domain,
            )
        except requests.RequestException as exc:
            print(f"Erro de comunicação com o Ollama: {exc}")
        except Exception as exc:
            print(f"Erro: {exc}")


if __name__ == "__main__":
    main()
