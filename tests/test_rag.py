from core.embeddings import (
    EmbeddingService
)
from core.vector_store import (
    VectorStore
)
from core.retriever import (
    ResearchRetriever
)
from core.rag_pipeline import (
    RAGPipeline
)
from core.citation_manager import (
    CitationManager
)
from services.llm_service import (
    LLMService
)


def main():

    print()
    print("=" * 70)
    print(
        "ResearchIQ Phase 3 - "
        "RAG System Test"
    )
    print("=" * 70)

    # --------------------------------------------------
    # Initialize components
    # --------------------------------------------------

    print(
        "\nInitializing embedding model..."
    )

    embedding_service = (
        EmbeddingService()
    )

    vector_store = (
        VectorStore()
    )

    print(
        f"\nKnowledge base vectors: "
        f"{vector_store.count()}"
    )

    if vector_store.count() == 0:

        print()
        print(
            "Knowledge base is empty."
        )

        print(
            "Run Phase 2 and ingest at least "
            "one research document first."
        )

        return

    retriever = (
        ResearchRetriever(
            embedding_service,
            vector_store
        )
    )

    print(
        "\nConnecting to Gemini..."
    )

    try:

        llm_service = (
            LLMService()
        )

    except Exception as exc:

        print()
        print(
            "LLM initialization failed:"
        )

        print(exc)

        return

    rag = (
        RAGPipeline(
            retriever,
            llm_service
        )
    )

    citation_manager = (
        CitationManager()
    )

    print(
        "\nResearchIQ RAG ready."
    )

    # --------------------------------------------------
    # Question loop
    # --------------------------------------------------

    while True:

        print()
        print("=" * 70)

        question = input(
            "\nAsk ResearchIQ "
            "(or type exit): "
        ).strip()

        if question.lower() in {
            "exit",
            "quit",
            "q"
        }:
            break

        if not question:
            continue

        print()
        print(
            "Retrieving evidence and "
            "generating answer..."
        )

        try:

            result = rag.ask(
                question
            )

        except Exception as exc:

            print()
            print(
                "RAG request failed:"
            )

            print(exc)

            continue

        # ----------------------------------------------
        # Answer
        # ----------------------------------------------

        print()
        print("=" * 70)
        print("RESEARCHIQ ANSWER")
        print("=" * 70)
        print()

        print(
            result["answer"]
        )

        # ----------------------------------------------
        # Sources
        # ----------------------------------------------

        print()
        print("=" * 70)
        print("RETRIEVED SOURCES")
        print("=" * 70)
        print()

        print(
            citation_manager.format_citation_list(
                result["sources"]
            )
        )

        # ----------------------------------------------
        # Retrieval details
        # ----------------------------------------------

        print()
        print("=" * 70)
        print("RETRIEVAL DETAILS")
        print("=" * 70)

        for source in result["sources"]:

            print()

            print(
                f"[{source['source_id']}]"
            )

            print(
                f"Document   : "
                f"{source['filename']}"
            )

            page = source.get(
                "page"
            )

            print(
                f"Page       : "
                f"{page if page is not None else 'N/A'}"
            )

            similarity = source.get(
                "similarity"
            )

            if similarity is not None:

                print(
                    f"Similarity : "
                    f"{similarity:.4f}"
                )

            print(
                f"Chunk      : "
                f"{source['chunk_index']}"
            )


if __name__ == "__main__":
    main()