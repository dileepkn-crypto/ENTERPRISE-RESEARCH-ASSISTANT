from typing import Dict, Optional

from core.retriever import (
    ResearchRetriever
)
from core.citation_manager import (
    CitationManager
)
from services.llm_service import (
    LLMService
)
from prompts.rag_prompt import (
    build_rag_prompt
)
from utils.config import TOP_K


class RAGPipeline:
    """
    Complete Retrieval-Augmented Generation
    pipeline for ResearchIQ.
    """

    def __init__(
        self,
        retriever: ResearchRetriever,
        llm_service: LLMService
    ):

        self.retriever = retriever
        self.llm_service = llm_service

        self.citation_manager = (
            CitationManager()
        )

    def ask(
        self,
        question: str,
        top_k: int = TOP_K,
        document_id: Optional[str] = None
    ) -> Dict:

        if not question or not question.strip():

            raise ValueError(
                "Question cannot be empty."
            )

        # ---------------------------------------------
        # 1. Retrieve evidence
        # ---------------------------------------------

        retrieved_chunks = (
            self.retriever.retrieve(
                query=question,
                top_k=top_k,
                document_id=document_id
            )
        )

        if not retrieved_chunks:

            return {
                "question":
                    question,

                "answer":
                    (
                        "The indexed research documents "
                        "do not provide sufficient "
                        "evidence to answer this question."
                    ),

                "sources":
                    [],

                "retrieved_chunks":
                    []
            }

        # ---------------------------------------------
        # 2. Build controlled context
        # ---------------------------------------------

        evidence_context = (
            self.citation_manager.build_context(
                retrieved_chunks
            )
        )

        # ---------------------------------------------
        # 3. Build grounded prompt
        # ---------------------------------------------

        prompt = build_rag_prompt(
            question=question,
            evidence_context=evidence_context
        )

        # ---------------------------------------------
        # 4. Generate
        # ---------------------------------------------

        answer = (
            self.llm_service.generate(
                prompt
            )
        )

        # ---------------------------------------------
        # 5. Build deterministic citations
        # ---------------------------------------------

        citations = (
            self.citation_manager.build_citations(
                retrieved_chunks
            )
        )

        return {
            "question":
                question,

            "answer":
                answer,

            "sources":
                citations,

            "retrieved_chunks":
                retrieved_chunks
        }