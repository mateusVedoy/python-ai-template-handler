import os
import numpy as np
from sentence_transformers import SentenceTransformer


class AiEmbedding:
    model: str
    task_type: str

    def __init__(self):
        model_name = os.getenv("EMBEDDING_MODEL")
        self.model = SentenceTransformer(model_name)
        self.task_type = "retrieval_document"

    def embed(self, chunks: list[str]):

        if not chunks:
            return np.array([])

        return self.model.encode(chunks, convert_to_numpy=True)
