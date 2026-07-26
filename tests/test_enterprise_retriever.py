from core.embeddings import EmbeddingService
from core.vector_store import VectorStore
from core.retriever import ResearchRetriever

from core.hybrid_retriever import HybridRetriever
from core.reranker import CrossEncoderReranker
from core.enterprise_retriever import EnterpriseRetriever


def main():

    print(
        "\nResearchIQ Enterprise Retrieval"
    )


    embeddings = (
        EmbeddingService()
    )

    vector_store = (
        VectorStore()
    )


    dense = ResearchRetriever(
        embeddings,
        vector_store
    )


    hybrid = HybridRetriever(
        dense,
        vector_store
    )


    reranker = (
        CrossEncoderReranker()
    )


    enterprise = (
        EnterpriseRetriever(
            hybrid,
            reranker
        )
    )


    query = input(
        "\nEnter research query: "
    )


    results = enterprise.retrieve(
        query,
        top_k=5
    )


    for index, result in enumerate(
        results,
        start=1
    ):

        print(
            "\n"
            + "=" * 70
        )

        print(
            f"[{index}] "
            f"{result.get('filename')}"
        )

        print(
            f"Page: "
            f"{result.get('page')}"
        )

        print(
            "Retrieval: "
            f"{result.get('retrieval_sources')}"
        )

        print(
            f"RRF: "
            f"{result.get('rrf_score', 0):.6f}"
        )

        print(
            f"Rerank score: "
            f"{result.get('rerank_score', 0):.6f}"
        )

        print()

        print(
            result.get(
                "text",
                ""
            )[:600]
        )


if __name__ == "__main__":
    main()