from services.paper_analyzer import PaperAnalyzer
from prompts.comparison_prompt import COMPARISON_PROMPT


class ComparisonService:
    """
    Compare two indexed academic papers using
    evidence stored in the ResearchIQ knowledge base.
    """

    def __init__(
        self,
        vector_store,
        llm_service
    ):

        self.vector_store = vector_store
        self.llm_service = llm_service

        self.paper_analyzer = PaperAnalyzer(
            vector_store,
            llm_service
        )


    def get_documents(self):

        return (
            self.paper_analyzer.get_documents()
        )


    def prepare_document_context(
        self,
        filename: str,
        max_characters: int = 30000
    ):

        chunks = (
            self.paper_analyzer
            .get_document_chunks(
                filename
            )
        )

        if not chunks:

            raise ValueError(
                f"No indexed evidence found "
                f"for {filename}."
            )

        context = (
            self.paper_analyzer
            .build_context(
                chunks,
                max_characters=max_characters
            )
        )

        return {
            "filename": filename,
            "chunks": chunks,
            "context": context
        }


    def compare(
        self,
        paper_a: str,
        paper_b: str
    ):

        if not paper_a or not paper_b:

            raise ValueError(
                "Two research papers must be selected."
            )

        if paper_a == paper_b:

            raise ValueError(
                "Select two different research papers."
            )

        # -------------------------------------------------
        # Prepare Paper A
        # -------------------------------------------------

        data_a = (
            self.prepare_document_context(
                paper_a
            )
        )

        # -------------------------------------------------
        # Prepare Paper B
        # -------------------------------------------------

        data_b = (
            self.prepare_document_context(
                paper_b
            )
        )

        # -------------------------------------------------
        # Build grounded comparison prompt
        # -------------------------------------------------

        prompt = COMPARISON_PROMPT.format(
            paper_a=paper_a,
            context_a=data_a["context"],

            paper_b=paper_b,
            context_b=data_b["context"]
        )

        # -------------------------------------------------
        # Gemini comparison
        # -------------------------------------------------

        comparison = (
            self.llm_service.generate(
                prompt
            )
        )

        return {
            "paper_a": paper_a,
            "paper_b": paper_b,

            "paper_a_chunks":
                len(data_a["chunks"]),

            "paper_b_chunks":
                len(data_b["chunks"]),

            "paper_a_context":
                len(data_a["context"]),

            "paper_b_context":
                len(data_b["context"]),

            "comparison":
                comparison
        }