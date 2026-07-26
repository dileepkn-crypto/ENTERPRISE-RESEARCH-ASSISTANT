from collections import Counter, defaultdict
from pathlib import Path


class AnalyticsService:
    """
    Compute deterministic analytics directly from
    ResearchIQ's ChromaDB metadata.

    No LLM is used for core statistics.
    """

    def __init__(self, vector_store):
        self.vector_store = vector_store


    # =====================================================
    # RAW DATA
    # =====================================================

    def get_raw_data(self):

        return self.vector_store.collection.get(
            include=[
                "documents",
                "metadatas"
            ]
        )


    # =====================================================
    # NORMALIZE DOCUMENT NAME
    # =====================================================

    @staticmethod
    def get_filename(metadata):

        if not metadata:
            return "Unknown Document"

        filename = (
            metadata.get("filename")
            or metadata.get("source")
            or metadata.get("document")
            or "Unknown Document"
        )

        return Path(
            str(filename)
        ).name


    # =====================================================
    # OVERVIEW STATISTICS
    # =====================================================

    def get_overview(self):

        data = self.get_raw_data()

        documents = data.get(
            "documents",
            []
        )

        metadatas = data.get(
            "metadatas",
            []
        )

        total_chunks = len(documents)

        filenames = []

        pages = set()

        for metadata in metadatas:

            metadata = metadata or {}

            filename = self.get_filename(
                metadata
            )

            filenames.append(
                filename
            )

            page = metadata.get("page")

            if page is not None:

                pages.add(
                    (
                        filename,
                        page
                    )
                )

        unique_documents = set(
            filenames
        )

        document_count = len(
            unique_documents
        )

        unique_pages = len(
            pages
        )

        average_chunks = (
            total_chunks / document_count
            if document_count
            else 0
        )

        return {
            "total_documents":
                document_count,

            "total_chunks":
                total_chunks,

            "unique_pages":
                unique_pages,

            "average_chunks":
                average_chunks
        }


    # =====================================================
    # DOCUMENT STATISTICS
    # =====================================================

    def get_document_statistics(self):

        data = self.get_raw_data()

        documents = data.get(
            "documents",
            []
        )

        metadatas = data.get(
            "metadatas",
            []
        )

        stats = defaultdict(
            lambda: {
                "chunks": 0,
                "pages": set(),
                "characters": 0
            }
        )

        for text, metadata in zip(
            documents,
            metadatas
        ):

            metadata = metadata or {}

            filename = self.get_filename(
                metadata
            )

            stats[filename]["chunks"] += 1

            stats[filename][
                "characters"
            ] += len(
                text or ""
            )

            page = metadata.get(
                "page"
            )

            if page is not None:

                stats[filename][
                    "pages"
                ].add(page)

        results = []

        for filename, values in stats.items():

            chunk_count = values[
                "chunks"
            ]

            character_count = values[
                "characters"
            ]

            average_chunk_length = (
                character_count
                / chunk_count
                if chunk_count
                else 0
            )

            results.append(
                {
                    "Document":
                        filename,

                    "Chunks":
                        chunk_count,

                    "Pages":
                        len(
                            values["pages"]
                        ),

                    "Characters":
                        character_count,

                    "Avg Chunk Length":
                        round(
                            average_chunk_length,
                            1
                        )
                }
            )

        results.sort(
            key=lambda item:
                item["Chunks"],
            reverse=True
        )

        return results


    # =====================================================
    # CHUNKS PER DOCUMENT
    # =====================================================

    def get_chunks_by_document(self):

        stats = (
            self.get_document_statistics()
        )

        return {
            item["Document"]:
                item["Chunks"]

            for item in stats
        }


    # =====================================================
    # PAGES PER DOCUMENT
    # =====================================================

    def get_pages_by_document(self):

        stats = (
            self.get_document_statistics()
        )

        return {
            item["Document"]:
                item["Pages"]

            for item in stats
        }


    # =====================================================
    # KNOWLEDGE DISTRIBUTION
    # =====================================================

    def get_knowledge_distribution(self):

        chunks = (
            self.get_chunks_by_document()
        )

        total = sum(
            chunks.values()
        )

        distribution = []

        for document, count in chunks.items():

            percentage = (
                (count / total) * 100
                if total
                else 0
            )

            distribution.append(
                {
                    "Document":
                        document,

                    "Chunks":
                        count,

                    "Knowledge Share (%)":
                        round(
                            percentage,
                            2
                        )
                }
            )

        return distribution


    # =====================================================
    # PAGE CHUNK DISTRIBUTION
    # =====================================================

    def get_page_distribution(self):

        data = self.get_raw_data()

        metadatas = data.get(
            "metadatas",
            []
        )

        page_counter = Counter()

        for metadata in metadatas:

            metadata = metadata or {}

            filename = self.get_filename(
                metadata
            )

            page = metadata.get(
                "page"
            )

            if page is not None:

                page_counter[
                    (
                        filename,
                        page
                    )
                ] += 1

        results = []

        for (
            filename,
            page
        ), count in page_counter.items():

            results.append(
                {
                    "Document":
                        filename,

                    "Page":
                        page,

                    "Chunks":
                        count
                }
            )

        results.sort(
            key=lambda item: (
                item["Document"],
                item["Page"]
            )
        )

        return results