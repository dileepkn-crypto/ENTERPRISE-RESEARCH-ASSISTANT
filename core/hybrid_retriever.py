import re
from pathlib import Path

from rank_bm25 import BM25Okapi


class HybridRetriever:
    """
    Hybrid retrieval combining:

    1. Dense semantic retrieval
    2. BM25 lexical retrieval
    3. Reciprocal Rank Fusion (RRF)
    """

    def __init__(
        self,
        dense_retriever,
        vector_store,
        rrf_k=60
    ):
        self.dense_retriever = dense_retriever
        self.vector_store = vector_store
        self.rrf_k = rrf_k

        self.documents = []
        self.metadatas = []
        self.ids = []

        self.bm25 = None

        self.refresh_index()


    # =====================================================
    # TOKENIZATION
    # =====================================================

    @staticmethod
    def tokenize(text):
        """
        Lightweight tokenizer for BM25.
        """

        if not text:
            return []

        return re.findall(
            r"\b[a-zA-Z0-9_\-\.]+\b",
            text.lower()
        )


    # =====================================================
    # BUILD BM25 INDEX
    # =====================================================

    def refresh_index(self):

        data = self.vector_store.collection.get(
            include=[
                "documents",
                "metadatas"
            ]
        )

        self.documents = data.get(
            "documents",
            []
        )

        self.metadatas = data.get(
            "metadatas",
            []
        )

        self.ids = data.get(
            "ids",
            []
        )

        if not self.documents:
            self.bm25 = None
            return

        tokenized_documents = [
            self.tokenize(document)
            for document
            in self.documents
        ]

        self.bm25 = BM25Okapi(
            tokenized_documents
        )


    # =====================================================
    # NORMALIZE RESULT
    # =====================================================

    @staticmethod
    def normalize_result(
        result,
        fallback_id
    ):

        metadata = result.get(
            "metadata",
            {}
        ) or {}

        filename = (
            result.get("filename")
            or metadata.get("filename")
            or metadata.get("source")
            or metadata.get("document")
            or "Unknown Document"
        )

        filename = Path(
            str(filename)
        ).name

        text = (
            result.get("text")
            or result.get("document")
            or result.get("content")
            or ""
        )

        chunk_id = (
            result.get("id")
            or metadata.get("chunk_id")
            or fallback_id
        )

        return {
            "id": str(chunk_id),
            "text": text,
            "filename": filename,
            "page": (
                result.get("page")
                or metadata.get("page")
            ),
            "metadata": metadata
        }


    # =====================================================
    # DENSE SEARCH
    # =====================================================

    def dense_search(
        self,
        query,
        top_k=10
    ):

        results = (
            self.dense_retriever.retrieve(
                query,
                top_k=top_k
            )
        )

        normalized = []

        for index, result in enumerate(
            results
        ):

            normalized.append(
                self.normalize_result(
                    result,
                    fallback_id=(
                        f"dense-{index}"
                    )
                )
            )

        return normalized


    # =====================================================
    # BM25 SEARCH
    # =====================================================

    def bm25_search(
        self,
        query,
        top_k=10
    ):

        if self.bm25 is None:
            return []

        query_tokens = self.tokenize(
            query
        )

        if not query_tokens:
            return []

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index:
                scores[index],
            reverse=True
        )[:top_k]

        results = []

        for index in ranked_indices:

            metadata = (
                self.metadatas[index]
                or {}
            )

            filename = (
                metadata.get("filename")
                or metadata.get("source")
                or metadata.get("document")
                or "Unknown Document"
            )

            filename = Path(
                str(filename)
            ).name

            results.append(
                {
                    "id": (
                        str(self.ids[index])
                        if index < len(self.ids)
                        else f"bm25-{index}"
                    ),

                    "text":
                        self.documents[index],

                    "filename":
                        filename,

                    "page":
                        metadata.get("page"),

                    "metadata":
                        metadata,

                    "bm25_score":
                        float(scores[index])
                }
            )

        return results


    # =====================================================
    # RESULT KEY
    # =====================================================

    @staticmethod
    def result_key(result):
        """
        Create a stable identity for RRF deduplication.
        """

        metadata = result.get(
            "metadata",
            {}
        ) or {}

        chunk_index = metadata.get(
            "chunk_index",
            metadata.get(
                "index"
            )
        )

        if chunk_index is not None:

            return (
                result.get("filename"),
                result.get("page"),
                chunk_index
            )

        return (
            result.get("filename"),
            result.get("page"),
            result.get("text", "")[:200]
        )


    # =====================================================
    # RECIPROCAL RANK FUSION
    # =====================================================

    def reciprocal_rank_fusion(
        self,
        dense_results,
        bm25_results
    ):

        fused = {}

        result_map = {}

        retrieval_sources = {}


        for source_name, results in [
            ("dense", dense_results),
            ("bm25", bm25_results)
        ]:

            for rank, result in enumerate(
                results,
                start=1
            ):

                key = self.result_key(
                    result
                )

                if key not in fused:

                    fused[key] = 0.0

                    result_map[key] = (
                        result.copy()
                    )

                    retrieval_sources[key] = []


                fused[key] += (
                    1.0
                    / (
                        self.rrf_k
                        + rank
                    )
                )

                retrieval_sources[
                    key
                ].append(
                    source_name
                )


        ranked_keys = sorted(
            fused,
            key=lambda key:
                fused[key],
            reverse=True
        )


        final_results = []

        for key in ranked_keys:

            result = result_map[
                key
            ]

            result["rrf_score"] = (
                fused[key]
            )

            result[
                "retrieval_sources"
            ] = retrieval_sources[
                key
            ]

            final_results.append(
                result
            )


        return final_results


    # =====================================================
    # HYBRID RETRIEVE
    # =====================================================

    def retrieve(
        self,
        query,
        top_k=5,
        candidate_k=12
    ):

        if not query or not query.strip():
            return []


        dense_results = (
            self.dense_search(
                query,
                top_k=candidate_k
            )
        )


        bm25_results = (
            self.bm25_search(
                query,
                top_k=candidate_k
            )
        )


        fused_results = (
            self.reciprocal_rank_fusion(
                dense_results,
                bm25_results
            )
        )


        return fused_results[
            :top_k
        ]