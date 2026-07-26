from pathlib import Path

from core.embeddings import (
    EmbeddingService
)
from core.vector_store import (
    VectorStore
)
from core.retriever import (
    ResearchRetriever
)
from services.ingestion_service import (
    IngestionService
)
from services.search_service import (
    SearchService
)


def clean_path(raw_path: str) -> str:

    path = raw_path.strip()

    if path.startswith("&"):
        path = path[1:].strip()

    path = path.strip('"')
    path = path.strip("'")

    return path


def main():

    print()
    print("=" * 65)
    print(
        "ResearchIQ Phase 2 - "
        "Semantic Retrieval Test"
    )
    print("=" * 65)

    # --------------------------------------------------
    # Initialize AI components
    # --------------------------------------------------

    print(
        "\nInitializing embedding model..."
    )

    embedding_service = (
        EmbeddingService()
    )

    print(
        "Embedding dimension:",
        embedding_service.embedding_dimension()
    )

    vector_store = (
        VectorStore()
    )

    retriever = (
        ResearchRetriever(
            embedding_service,
            vector_store
        )
    )

    ingestion_service = (
        IngestionService(
            embedding_service,
            vector_store
        )
    )

    search_service = (
        SearchService(
            retriever
        )
    )

    # --------------------------------------------------
    # Ingestion
    # --------------------------------------------------

    print()
    print(
        "Current vectors in knowledge base:",
        vector_store.count()
    )

    choice = input(
        "\nIngest a document? (y/n): "
    ).strip().lower()

    if choice == "y":

        raw_path = input(
            "\nEnter document path: "
        )

        document_path = clean_path(
            raw_path
        )

        path = Path(
            document_path
        )

        if not path.exists():

            print(
                f"\nFile not found: {path}"
            )

            return

        try:

            result = (
                ingestion_service.ingest(
                    path
                )
            )

        except Exception as exc:

            print(
                "\nIngestion failed:"
            )

            print(exc)

            return

        print()
        print("=" * 65)
        print("INGESTION COMPLETE")
        print("=" * 65)

        print(
            f"Document : "
            f"{result['filename']}"
        )

        print(
            f"ID       : "
            f"{result['document_id']}"
        )

        print(
            f"Pages    : "
            f"{result['pages']}"
        )

        print(
            f"Chunks   : "
            f"{result['chunks']}"
        )

        print(
            f"Stored   : "
            f"{result['stored']}"
        )

    # --------------------------------------------------
    # Search loop
    # --------------------------------------------------

    if vector_store.count() == 0:

        print(
            "\nKnowledge base is empty."
        )

        return

    print()
    print(
        "Knowledge base vectors:",
        vector_store.count()
    )

    while True:

        print()
        print("=" * 65)

        query = input(
            "\nAsk a research question "
            "(or type exit): "
        ).strip()

        if query.lower() in {
            "exit",
            "quit",
            "q"
        }:
            break

        if not query:
            continue

        results = (
            search_service.search(
                query=query,
                top_k=5
            )
        )

        print()
        print("=" * 65)
        print("SEMANTIC SEARCH RESULTS")
        print("=" * 65)

        if not results:

            print(
                "No results found."
            )

            continue

        for index, result in enumerate(
            results,
            start=1
        ):

            print()
            print(
                f"RESULT #{index}"
            )

            print(
                f"Document   : "
                f"{result['filename']}"
            )

            page = result.get(
                "page"
            )

            print(
                f"Page       : "
                f"{page if page is not None else 'N/A'}"
            )

            print(
                f"Chunk      : "
                f"{result['chunk_index']}"
            )

            print(
                f"Similarity : "
                f"{result['similarity']:.4f}"
            )

            print(
                f"Distance   : "
                f"{result['distance']:.4f}"
            )

            print("-" * 65)

            preview = (
                result["text"][:700]
            )

            print(preview)

            print()
            print("-" * 65)


if __name__ == "__main__":
    main()