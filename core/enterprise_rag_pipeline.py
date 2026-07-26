class EnterpriseRAGPipeline:

    def __init__(
        self,
        retriever,
        llm_service,
        relevance_guard
    ):
        self.retriever = retriever
        self.llm_service = llm_service
        self.relevance_guard = relevance_guard


    def build_context(self, results):

        context_blocks = []

        for index, result in enumerate(
            results,
            start=1
        ):

            filename = result.get(
                "filename",
                "Unknown Document"
            )

            page = result.get(
                "page",
                "N/A"
            )

            text = result.get(
                "text",
                ""
            )

            block = (
                f"[S{index}]\n"
                f"Document: {filename}\n"
                f"Page: {page}\n"
                f"Evidence:\n{text}\n"
            )

            context_blocks.append(
                block
            )

        return "\n\n".join(
            context_blocks
        )


    def build_prompt(
        self,
        question,
        context
    ):

        return f"""
You are ResearchIQ, an evidence-grounded academic
research assistant.

Answer the user's question using ONLY the retrieved
research evidence below.

STRICT RULES:

1. Do not use outside knowledge.

2. Do not invent information.

3. Every important factual claim should be supported
   by the supplied evidence.

4. Cite evidence using source identifiers such as:
   [S1], [S2], [S3].

5. Never create a source identifier that does not
   exist in the supplied evidence.

6. If the evidence does not contain enough information
   to answer part of the question, explicitly say so.

7. Distinguish evidence-supported conclusions from
   interpretations.

QUESTION:

{question}

RETRIEVED RESEARCH EVIDENCE:

{context}

ANSWER:
"""


    def prepare_sources(self, results):

        sources = []

        for index, result in enumerate(
            results,
            start=1
        ):

            sources.append(
                {
                    "source_id":
                        f"S{index}",

                    "filename":
                        result.get(
                            "filename",
                            "Unknown Document"
                        ),

                    "page":
                        result.get(
                            "page"
                        ),

                    "text":
                        result.get(
                            "text",
                            ""
                        ),

                    "rrf_score":
                        result.get(
                            "rrf_score"
                        ),

                    "rerank_score":
                        result.get(
                            "rerank_score"
                        ),

                    "retrieval_sources":
                        result.get(
                            "retrieval_sources",
                            []
                        )
                }
            )

        return sources


    def ask(
        self,
        question,
        top_k=5
    ):

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        question = question.strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )


        # =============================================
        # ENTERPRISE RETRIEVAL
        # =============================================

        results = self.retriever.retrieve(
            question,
            top_k=top_k
        )


        # =============================================
        # RELEVANCE GUARD
        # =============================================

        guard_result = (
            self.relevance_guard.evaluate(
                results
            )
        )


        if not guard_result["allowed"]:

            return {
                "answer": (
                    "I could not find sufficiently "
                    "relevant evidence in the indexed "
                    "research library to answer this "
                    "question reliably."
                ),

                "sources": [],

                "grounded": False,

                "guard_reason":
                    guard_result["reason"],

                "retrieved_results":
                    results
            }


        relevant_results = (
            guard_result[
                "relevant_results"
            ][:top_k]
        )


        # =============================================
        # CONTEXT
        # =============================================

        context = self.build_context(
            relevant_results
        )


        # =============================================
        # PROMPT
        # =============================================

        prompt = self.build_prompt(
            question,
            context
        )


        # =============================================
        # GENERATION
        # =============================================

        answer = (
            self.llm_service.generate(
                prompt
            )
        )


        # =============================================
        # SOURCES
        # =============================================

        sources = self.prepare_sources(
            relevant_results
        )


        return {
            "answer": answer,
            "sources": sources,
            "grounded": True,
            "guard_reason":
                guard_result["reason"],
            "retrieved_results":
                results
        }