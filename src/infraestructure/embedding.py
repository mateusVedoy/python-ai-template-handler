import google.generativeai as genai
import os
import numpy as np


class AiEmbedding:
    model: str
    task_type: str

    def __init__(self):
        self.model = os.getenv("GEMINI_EMBEDDING_MODEL")
        self.task_type = "retrieval_document"

    def embed(self, chunks: list[str]):

        if len(chunks) == 0:
            return np.array([])

        return genai.embed_content(
            model=self.model,
            content=chunks,
            task_type=self.task_type
        )["embedding"]
