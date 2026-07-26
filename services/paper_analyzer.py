from pathlib import Path

from prompts.analysis_prompt import PAPER_ANALYSIS_PROMPT


class PaperAnalyzer:

    def __init__(
        self,
        vector_store,
        llm_service
    ):
        self.vector_store = vector_store
        self.llm_service = llm_service


    def get_documents(self):
        """
        Return unique filenames currently stored
        in the vector database.
        """

        data = self.vector_store.collection.get(
            include=["metadatas"]
        )

        documents = set()

        for metadata in data.get(
            "metadatas",
            []
        ):
            if not metadata:
                continue

            filename = (
                metadata.get("filename")
                or metadata.get("source")
                or metadata.get("document")
            )

            if filename:
                documents.add(
                    Path(str(filename)).name
                )

        return sorted(documents)


    def get_document_chunks(
        self,
        filename: str
    ):
        """
        Retrieve all chunks belonging to one document.
        """

        data = self.vector_store.collection.get(
            include=[
                "documents",
                "metadatas"
            ]
        )

        chunks = []

        documents = data.get(
            "documents",
            []
        )

        metadatas = data.get(
            "metadatas",
            []
        )

        for text, metadata in zip(
            documents,
            metadatas
        ):
            metadata = metadata or {}

            stored_name = (
                metadata.get("filename")
                or metadata.get("source")
                or metadata.get("document")
            )

            if not stored_name:
                continue

            stored_name = Path(
                str(stored_name)
            ).name

            if stored_name == filename:

                chunks.append(
                    {
                        "text": text,
                        "page": metadata.get(
                            "page"
                        ),
                        "chunk_index": metadata.get(
                            "chunk_index",
                            metadata.get(
                                "index",
                                0
                            )
                        )
                    }
                )

        chunks.sort(
            key=lambda item: (
                item.get("page") or 0,
                item.get("chunk_index") or 0
            )
        )

        return chunks


    def build_context(
        self,
        chunks,
        max_characters=45000
    ):
        """
        Construct bounded evidence context.

        The limit prevents extremely large papers from
        being passed blindly to the LLM.
        """

        context_parts = []
        current_length = 0

        for chunk in chunks:

            page = chunk.get(
                "page",
                "N/A"
            )

            text = chunk.get(
                "text",
                ""
            )

            block = (
                f"\n[Page {page}]\n"
                f"{text}\n"
            )

            if (
                current_length
                + len(block)
                > max_characters
            ):
                break

            context_parts.append(block)

            current_length += len(block)

        return "\n".join(
            context_parts
        )


    def analyze(
        self,
        filename: str
    ):

        chunks = self.get_document_chunks(
            filename
        )

        if not chunks:
            raise ValueError(
                "No indexed chunks were found "
                f"for {filename}."
            )

        context = self.build_context(
            chunks
        )

        prompt = (
            PAPER_ANALYSIS_PROMPT.format(
                document=filename,
                context=context
            )
        )

        analysis = self.llm_service.generate(
            prompt
        )

        return {
            "filename": filename,
            "analysis": analysis,
            "chunks_analyzed": len(chunks),
            "context_characters": len(context)
        }