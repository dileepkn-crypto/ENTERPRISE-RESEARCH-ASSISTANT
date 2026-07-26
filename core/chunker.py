from typing import Dict, List
import hashlib

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from core.text_cleaner import is_valid_text
from utils.config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


class DocumentChunker:
    """
    Split extracted document pages into retrieval-ready chunks
    while preserving document metadata.
    """

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP
    ):

        if chunk_size <= 0:
            raise ValueError(
                "chunk_size must be greater than 0."
            )

        if chunk_overlap < 0:
            raise ValueError(
                "chunk_overlap cannot be negative."
            )

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,

            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                "; ",
                ", ",
                " ",
                ""
            ],

            length_function=len
        )

    def chunk_documents(
        self,
        documents: List[Dict]
    ) -> List[Dict]:

        all_chunks = []

        for document in documents:

            chunks = self.chunk_document(
                document
            )

            all_chunks.extend(
                chunks
            )

        return all_chunks

    def chunk_document(
        self,
        document: Dict
    ) -> List[Dict]:

        text = document.get(
            "text",
            ""
        )

        if not is_valid_text(text):
            return []

        split_texts = self.splitter.split_text(
            text
        )

        chunks = []

        for chunk_index, chunk_text in enumerate(
            split_texts
        ):

            chunk_text = chunk_text.strip()

            if not is_valid_text(chunk_text):
                continue

            chunk_id = self._generate_chunk_id(
                document_id=document["document_id"],
                page=document.get("page"),
                chunk_index=chunk_index,
                text=chunk_text
            )

            chunk = {
                "chunk_id": chunk_id,

                "document_id":
                    document["document_id"],

                "filename":
                    document["filename"],

                "file_type":
                    document["file_type"],

                "page":
                    document.get("page"),

                "total_pages":
                    document.get("total_pages"),

                "chunk_index":
                    chunk_index,

                "text":
                    chunk_text
            }

            chunks.append(chunk)

        return chunks

    @staticmethod
    def _generate_chunk_id(
        document_id: str,
        page,
        chunk_index: int,
        text: str
    ) -> str:

        raw = (
            f"{document_id}|"
            f"{page}|"
            f"{chunk_index}|"
            f"{text}"
        )

        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()[:20]