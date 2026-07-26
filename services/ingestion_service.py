from pathlib import Path
from typing import Dict

from core.document_processor import (
    DocumentProcessor
)
from core.chunker import (
    DocumentChunker
)
from core.embeddings import (
    EmbeddingService
)
from core.vector_store import (
    VectorStore
)


class IngestionService:
    """
    Complete research-document ingestion pipeline.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore
    ):

        self.processor = (
            DocumentProcessor()
        )

        self.chunker = (
            DocumentChunker()
        )

        self.embedding_service = (
            embedding_service
        )

        self.vector_store = (
            vector_store
        )

    def ingest(
        self,
        file_path: str | Path
    ) -> Dict:

        file_path = Path(
            file_path
        )

        print(
            f"\nProcessing: {file_path.name}"
        )

        # ----------------------------------------------
        # 1. Extract
        # ----------------------------------------------

        pages = (
            self.processor.process_document(
                file_path
            )
        )

        if not pages:
            raise ValueError(
                "No readable text was extracted "
                "from the document."
            )

        print(
            f"Readable pages/sections: "
            f"{len(pages)}"
        )

        # ----------------------------------------------
        # 2. Chunk
        # ----------------------------------------------

        chunks = (
            self.chunker.chunk_documents(
                pages
            )
        )

        if not chunks:
            raise ValueError(
                "No valid chunks were generated."
            )

        print(
            f"Generated chunks: "
            f"{len(chunks)}"
        )

        # ----------------------------------------------
        # 3. Embed
        # ----------------------------------------------

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        print(
            "Generating embeddings..."
        )

        embeddings = (
            self.embedding_service.embed_texts(
                texts
            )
        )

        # ----------------------------------------------
        # 4. Store
        # ----------------------------------------------

        stored = (
            self.vector_store.add_chunks(
                chunks,
                embeddings
            )
        )

        print(
            f"Stored vectors: {stored}"
        )

        # All pages/chunks share the same
        # document ID.
        document_id = chunks[0][
            "document_id"
        ]

        return {
            "document_id":
                document_id,

            "filename":
                file_path.name,

            "pages":
                len(pages),

            "chunks":
                len(chunks),

            "stored":
                stored
        }