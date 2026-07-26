from typing import List, Union

import numpy as np
from sentence_transformers import SentenceTransformer

from utils.config import EMBEDDING_MODEL


class EmbeddingService:
    """
    Generate semantic vector embeddings for
    research document chunks and user queries.
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name

        print(f"Loading embedding model: {model_name}")

        self.model = SentenceTransformer(model_name)

        print("Embedding model loaded successfully.")

    def embed_texts(
        self,
        texts: List[str]
    ) -> List[List[float]]:

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=len(texts) > 10
        )

        return embeddings.astype(
            np.float32
        ).tolist()

    def embed_query(
        self,
        query: str
    ) -> List[float]:

        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        embedding = self.model.encode(
            query.strip(),
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding.astype(
            np.float32
        ).tolist()

    def embedding_dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()