from core.embeddings import EmbeddingService
from core.vector_store import VectorStore
from core.retriever import ResearchRetriever

from core.hybrid_retriever import HybridRetriever
from core.reranker import CrossEncoderReranker
from core.enterprise_retriever import EnterpriseRetriever
from core.relevance_guard import RelevanceGuard
from core.enterprise_rag_pipeline import EnterpriseRAGPipeline

from services.llm_service import LLMService


def main():

    print(
        "\nResearchIQ Enterprise RAG"
    )


    embeddings = EmbeddingService()

    vector_store = VectorStore()


    dense = ResearchRetriever(
        embeddings,
        vector_store
    )


    hybrid = HybridRetriever(
        dense,
        vector_store
    )


    reranker = CrossEncoderReranker()


    enterprise_retriever = (
        EnterpriseRetriever(
            hybrid,
            reranker
        )
    )


    guard = RelevanceGuard(
        minimum_score=-2.0
    )


    llm = LLMService()


    rag = EnterpriseRAGPipeline(
        enterprise_retriever,
        llm,
        guard
    )


    while True:

        question = input(
            "\nAsk ResearchIQ "
            "(or 'exit'): "
        ).strip()


        if question.lower() == "exit":
            break


        if not question:
            continue


        print(
            "\nRetrieving evidence..."
        )


        result = rag.ask(
            question
        )


        print(
            "\n"
            + "=" * 70
        )

        print("ANSWER")

        print("=" * 70)

        print(
            result["answer"]
        )


        print(
            "\nGrounded:",
            result["grounded"]
        )


        print(
            "Guard:",
            result["guard_reason"]
        )


        if result["sources"]:

            print(
                "\nSOURCES"
            )

            for source in result[
                "sources"
            ]:

                print(
                    "\n"
                    f"[{source['source_id']}] "
                    f"{source['filename']}"
                )

                print(
                    "Page:",
                    source["page"]
                )

                print(
                    "Rerank:",
                    source[
                        "rerank_score"
                    ]
                )


if __name__ == "__main__":
    main()