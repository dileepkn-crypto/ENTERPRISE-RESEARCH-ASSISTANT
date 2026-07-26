from typing import Dict, List


class CitationManager:
    """
    Creates deterministic citation mappings
    from retrieved research chunks.
    """

    @staticmethod
    def build_context(
        retrieved_chunks: List[Dict]
    ) -> str:

        context_blocks = []

        for index, chunk in enumerate(
            retrieved_chunks,
            start=1
        ):
            source_id = f"S{index}"

            filename = chunk.get(
                "filename",
                "Unknown document"
            )

            page = chunk.get("page")

            page_display = (
                str(page)
                if page is not None
                else "N/A"
            )

            text = chunk.get(
                "text",
                ""
            )

            block = f"""
[{source_id}]

Document: {filename}
Page: {page_display}

Evidence:
{text}
""".strip()

            context_blocks.append(block)

        return "\n\n------------------------------\n\n".join(
            context_blocks
        )

    @staticmethod
    def build_citations(
        retrieved_chunks: List[Dict]
    ) -> List[Dict]:

        citations = []

        for index, chunk in enumerate(
            retrieved_chunks,
            start=1
        ):
            citations.append(
                {
                    "source_id": f"S{index}",
                    "filename": chunk.get("filename"),
                    "page": chunk.get("page"),
                    "chunk_id": chunk.get("chunk_id"),
                    "chunk_index": chunk.get("chunk_index"),
                    "similarity": chunk.get("similarity"),
                    "text": chunk.get("text")
                }
            )

        return citations

    @staticmethod
    def format_citation_list(
        citations: List[Dict]
    ) -> str:

        if not citations:
            return "No sources retrieved."

        lines = []

        for citation in citations:

            source_id = citation["source_id"]

            filename = (
                citation.get("filename")
                or "Unknown document"
            )

            page = citation.get("page")

            if page is not None:
                source = (
                    f"[{source_id}] "
                    f"{filename} — Page {page}"
                )
            else:
                source = (
                    f"[{source_id}] "
                    f"{filename}"
                )

            lines.append(source)

        return "\n".join(lines)