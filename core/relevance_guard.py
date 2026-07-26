class RelevanceGuard:
    """
    Evaluates reranked retrieval results before
    sending evidence to the LLM.

    Cross-encoder scores are ranking scores,
    not probabilities or calibrated confidence.
    """

    def __init__(
        self,
        minimum_score=-2.0,
        minimum_relevant_results=1
    ):
        self.minimum_score = minimum_score
        self.minimum_relevant_results = (
            minimum_relevant_results
        )


    def evaluate(self, results):

        if not results:
            return {
                "allowed": False,
                "reason": "No evidence retrieved.",
                "relevant_results": []
            }

        relevant_results = []

        for result in results:

            score = result.get(
                "rerank_score"
            )

            if score is None:
                continue

            if score >= self.minimum_score:
                relevant_results.append(
                    result
                )

        allowed = (
            len(relevant_results)
            >= self.minimum_relevant_results
        )

        if allowed:
            reason = (
                "Relevant evidence was retrieved."
            )
        else:
            reason = (
                "Retrieved evidence did not meet "
                "the configured relevance threshold."
            )

        return {
            "allowed": allowed,
            "reason": reason,
            "relevant_results":
                relevant_results
        }