from typing import Dict, List, Optional

from core.retriever import ResearchRetriever


class SearchService:
    """
    Application-level semantic search service.
    """

    def __init__(
        self,
        retriever: ResearchRetriever
    ):

        self.retriever = retriever

    def search(
        self,
        query: str,
        top_k: int = 5,
        document_id: Optional[str] = None
    ) -> List[Dict]:

        return self.retriever.retrieve(
            query=query,
            top_k=top_k,
            document_id=document_id
        )