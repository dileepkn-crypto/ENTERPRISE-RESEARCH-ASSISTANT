class EnterpriseRetriever:
    """
    ResearchIQ retrieval pipeline:

    Dense Retrieval
          +
    BM25 Retrieval
          ↓
    Reciprocal Rank Fusion
          ↓
    Cross-Encoder Reranking
    """

    def __init__(
        self,
        hybrid_retriever,
        reranker
    ):

        self.hybrid_retriever = (
            hybrid_retriever
        )

        self.reranker = (
            reranker
        )


    def retrieve(
        self,
        query,
        top_k=5,
        candidate_k=15
    ):

        candidates = (
            self.hybrid_retriever.retrieve(
                query=query,
                top_k=candidate_k,
                candidate_k=max(
                    candidate_k,
                    20
                )
            )
        )


        results = (
            self.reranker.rerank(
                query=query,
                results=candidates,
                top_k=top_k
            )
        )


        return results