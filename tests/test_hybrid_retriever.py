from core.embeddings import EmbeddingService
from core.vector_store import VectorStore
from core.retriever import ResearchRetriever
from core.hybrid_retriever import HybridRetriever


def main():

    print(
        "\nInitializing ResearchIQ Hybrid Retrieval..."
    )

    embedding_service = (
        EmbeddingService()
    )

    vector_store = (
        VectorStore()
    )

    dense_retriever = (
        ResearchRetriever(
            embedding_service,
            vector_store
        )
    )

    hybrid_retriever = (
        HybridRetriever(
            dense_retriever,
            vector_store
        )
    )


    print(
        f"Indexed vectors: "
        f"{vector_store.count()}"
    )


    while True:

        query = input(
            "\nResearch query "
            "(or 'exit'): "
        ).strip()

        if query.lower() == "exit":
            break

        if not query:
            continue


        results = (
            hybrid_retriever.retrieve(
                query=query,
                top_k=5
            )
        )


        print(
            "\n"
            + "=" * 70
        )

        print(
            "HYBRID RETRIEVAL RESULTS"
        )

        print(
            "=" * 70
        )


        for index, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n[{index}] "
                f"{result['filename']}"
            )

            print(
                f"Page: "
                f"{result.get('page')}"
            )

            print(
                "Retrieved by: "
                f"{', '.join(result['retrieval_sources'])}"
            )

            print(
                f"RRF score: "
                f"{result['rrf_score']:.6f}"
            )

            print(
                "\n"
                f"{result['text'][:500]}"
            )

            print(
                "\n"
                + "-" * 70
            )


if __name__ == "__main__":
    main()