from typing import Dict, List, Optional

from core.embeddings import EmbeddingService
from core.vector_store import VectorStore
from utils.config import TOP_K


class ResearchRetriever:
    """
    Semantic retrieval layer for ResearchIQ.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore
    ):

        self.embedding_service = (
            embedding_service
        )

        self.vector_store = (
            vector_store
        )

    def retrieve(
        self,
        query: str,
        top_k: int = TOP_K,
        document_id: Optional[str] = None
    ) -> List[Dict]:

        if not query or not query.strip():
            return []

        query_embedding = (
            self.embedding_service.embed_query(
                query
            )
        )

        where = None

        if document_id:
            where = {
                "document_id":
                    document_id
            }

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            where=where
        )

        return self._format_results(
            results
        )

    @staticmethod
    def _format_results(
        results: Dict
    ) -> List[Dict]:

        if not results:
            return []

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        distances = results.get(
            "distances",
            [[]]
        )[0]

        ids = results.get(
            "ids",
            [[]]
        )[0]

        formatted_results = []

        for (
            chunk_id,
            document,
            metadata,
            distance
        ) in zip(
            ids,
            documents,
            metadatas,
            distances
        ):

            # With cosine distance:
            # smaller distance = more similar.
            #
            # This is a convenient transformed score,
            # not a calibrated probability/confidence.
            similarity = max(
                0.0,
                min(
                    1.0,
                    1.0 - float(distance)
                )
            )

            formatted_results.append(
                {
                    "chunk_id":
                        chunk_id,

                    "text":
                        document,

                    "document_id":
                        metadata.get(
                            "document_id"
                        ),

                    "filename":
                        metadata.get(
                            "filename"
                        ),

                    "file_type":
                        metadata.get(
                            "file_type"
                        ),

                    "page":
                        metadata.get(
                            "page"
                        ),

                    "chunk_index":
                        metadata.get(
                            "chunk_index"
                        ),

                    "distance":
                        float(distance),

                    "similarity":
                        similarity
                }
            )

        return formatted_results