from __future__ import annotations

from typing import Any

import chromadb
import requests


CHROMA_DIR = "data/chroma"
COLLECTION_NAME = "university_books"

CHAT_MODEL = "qwen3:4b"
EMBEDDING_MODEL = "embeddinggemma"

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"

TOP_K = 5


def embed_query(query: str) -> list[float]:
    response = requests.post(
        OLLAMA_EMBED_URL,
        json={
            "model": EMBEDDING_MODEL,
            "input": query,
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()
    embeddings = data.get("embeddings")

    if not embeddings:
        raise RuntimeError("O Ollama não retornou o embedding da pergunta.")

    return embeddings[0]


def retrieve(
    collection: Any,
    question: str,
    top_k: int = TOP_K,
) -> list[dict[str, Any]]:
    query_embedding = embed_query(question)

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]
    distances = result["distances"][0]

    sources: list[dict[str, Any]] = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
        strict=True,
    ):
        sources.append(
            {
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return sources


def build_context(
    sources: list[dict[str, Any]],
) -> str:
    blocks: list[str] = []

    for index, source in enumerate(sources, start=1):
        metadata = source["metadata"]

        block = "\n".join(
            [
                f"[Fonte {index}]",
                f"Arquivo: {metadata['source']}",
                f"Página: {metadata['page']}",
                f"Trecho: {source['text']}",
            ]
        )

        blocks.append(block)

    return "\n\n".join(blocks)


def generate_answer(
    question: str,
    context: str,
) -> str:
    system_prompt = """
Você é um tutor universitário especializado em algoritmos,
engenharia de software e ética.

Responda somente com base no contexto fornecido.

Regras:
1. Não invente informações ausentes no contexto.
2. Cite as fontes usando o formato [Fonte 1], [Fonte 2].
3. Quando não houver evidência suficiente, diga claramente:
   "Não encontrei evidência suficiente nos documentos."
4. Diferencie a explicação do autor de sua própria síntese.
5. Não reproduza longos trechos literalmente.
6. Responda em português brasileiro.
""".strip()

    user_prompt = f"""
CONTEXTO RECUPERADO:

{context}

PERGUNTA:

{question}
""".strip()

    response = requests.post(
        OLLAMA_CHAT_URL,
        json={
            "model": CHAT_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_ctx": 4096,
            },
        },
        timeout=600,
    )

    response.raise_for_status()

    data = response.json()

    return data["message"]["content"]


def load_collection() -> Any:
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    try:
        return client.get_collection(COLLECTION_NAME)
    except Exception as exc:
        raise RuntimeError(
            "A coleção do RAG ainda não existe. "
            "Execute primeiro:\n"
            "uv run python -m src.rag.ingest"
        ) from exc


def main() -> None:
    collection = load_collection()

    print()
    print("RAG universitário local")
    print("Digite 'sair' para encerrar.")
    print()

    while True:
        question = input("Você: ").strip()

        if question.lower() in {
            "sair",
            "exit",
            "quit",
        }:
            print("Encerrando o RAG.")
            break

        if not question:
            continue

        try:
            sources = retrieve(
                collection=collection,
                question=question,
            )

            context = build_context(sources)

            answer = generate_answer(
                question=question,
                context=context,
            )

            print()
            print("Assistente:")
            print(answer)
            print()

            print("Trechos recuperados:")

            for index, source in enumerate(
                sources,
                start=1,
            ):
                metadata = source["metadata"]
                distance = source["distance"]

                print(
                    f"[{index}] "
                    f"{metadata['source']} "
                    f"— página {metadata['page']} "
                    f"— distância {distance:.4f}"
                )

            print()

        except requests.RequestException as exc:
            print()
            print("Erro ao acessar o Ollama. Confirme se o serviço está ativo.")
            print(f"Detalhes: {exc}")
            print()

        except Exception as exc:
            print()
            print(f"Erro: {exc}")
            print()


if __name__ == "__main__":
    main()
