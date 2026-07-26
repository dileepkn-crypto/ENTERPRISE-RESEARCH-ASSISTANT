from services.paper_analyzer import PaperAnalyzer
from prompts.gap_prompt import GAP_ANALYSIS_PROMPT


class GapFinderService:
    """
    Cross-document research opportunity analysis.

    Uses evidence from indexed papers and distinguishes
    document-supported limitations from AI-synthesized
    candidate research opportunities.
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


    # =====================================================
    # DOCUMENTS
    # =====================================================

    def get_documents(self):

        return self.paper_analyzer.get_documents()


    # =====================================================
    # DOCUMENT CONTEXT
    # =====================================================

    def prepare_document_context(
        self,
        filename: str,
        max_characters: int = 18000
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


    # =====================================================
    # BUILD MULTI-PAPER CONTEXT
    # =====================================================

    def build_research_context(
        self,
        filenames
    ):

        context_blocks = []

        document_stats = []

        for index, filename in enumerate(
            filenames,
            start=1
        ):

            data = (
                self.prepare_document_context(
                    filename
                )
            )

            block = (
                "\n"
                "==================================================\n"
                f"DOCUMENT {index}\n"
                "==================================================\n"
                f"Filename: {filename}\n\n"
                f"{data['context']}\n"
            )

            context_blocks.append(
                block
            )

            document_stats.append(
                {
                    "filename": filename,
                    "chunks": len(
                        data["chunks"]
                    ),
                    "context_characters": len(
                        data["context"]
                    )
                }
            )

        return (
            "\n".join(context_blocks),
            document_stats
        )


    # =====================================================
    # GAP ANALYSIS
    # =====================================================

    def analyze(
        self,
        filenames
    ):

        if not filenames:

            raise ValueError(
                "Select research papers for analysis."
            )

        if len(filenames) < 2:

            raise ValueError(
                "Research gap analysis requires "
                "at least two papers."
            )

        research_context, stats = (
            self.build_research_context(
                filenames
            )
        )

        prompt = (
            GAP_ANALYSIS_PROMPT.format(
                research_context=research_context
            )
        )

        analysis = (
            self.llm_service.generate(
                prompt
            )
        )

        return {
            "documents": filenames,
            "document_count": len(
                filenames
            ),
            "document_stats": stats,
            "context_characters": len(
                research_context
            ),
            "analysis": analysis
        }