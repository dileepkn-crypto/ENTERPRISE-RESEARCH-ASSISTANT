from typing import Dict, List, Optional

import chromadb

from utils.config import CHROMA_PATH


class VectorStore:
    """
    Persistent ChromaDB vector store for ResearchIQ.
    """

    COLLECTION_NAME = "research_knowledge"

    def __init__(
        self,
        collection_name: str = COLLECTION_NAME
    ):

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PATH)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name,
                metadata={
                    "hnsw:space": "cosine"
                }
            )
        )

    # --------------------------------------------------
    # Add chunks
    # --------------------------------------------------

    def add_chunks(
        self,
        chunks: List[Dict],
        embeddings: List[List[float]]
    ) -> int:

        if not chunks:
            return 0

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks must match "
                "number of embeddings."
            )

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:

            ids.append(
                chunk["chunk_id"]
            )

            documents.append(
                chunk["text"]
            )

            # Chroma metadata values should be
            # simple scalar values.
            metadata = {
                "document_id":
                    str(chunk["document_id"]),

                "filename":
                    str(chunk["filename"]),

                "file_type":
                    str(chunk["file_type"]),

                "chunk_index":
                    int(chunk["chunk_index"])
            }

            page = chunk.get("page")

            if page is not None:
                metadata["page"] = int(page)

            total_pages = chunk.get(
                "total_pages"
            )

            if total_pages is not None:
                metadata["total_pages"] = int(
                    total_pages
                )

            metadatas.append(metadata)

        # upsert makes repeated ingestion safer than add()
        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        return len(ids)

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        where: Optional[Dict] = None
    ) -> Dict:

        count = self.count()

        if count == 0:
            return {
                "ids": [[]],
                "documents": [[]],
                "metadatas": [[]],
                "distances": [[]]
            }

        top_k = min(
            top_k,
            count
        )

        query_args = {
            "query_embeddings": [
                query_embedding
            ],
            "n_results": top_k,
            "include": [
                "documents",
                "metadatas",
                "distances"
            ]
        }

        if where:
            query_args["where"] = where

        return self.collection.query(
            **query_args
        )

    # --------------------------------------------------
    # Delete document
    # --------------------------------------------------

    def delete_document(
        self,
        document_id: str
    ) -> None:

        self.collection.delete(
            where={
                "document_id":
                    document_id
            }
        )

    # --------------------------------------------------
    # Utility
    # --------------------------------------------------

    def count(self) -> int:
        return self.collection.count()

    def reset_collection(self) -> None:

        name = self.collection.name

        self.client.delete_collection(
            name=name
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=name,
                metadata={
                    "hnsw:space": "cosine"
                }
            )
        )