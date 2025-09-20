from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import os


class AiSemantic:
    embedding: str
    task_type: str

    def __init__(self):
        embedding_model = os.getenv("EMBEDDING_MODEL")
        self.embedding = SentenceTransformer(embedding_model)
        self.task_type = "retrieval_query"

    def find_relevant_chunks(self, prompt, chunks, embed_chunk, top_k=3) -> list:

        if len(chunks) == 0:
            return []

        query_embedding = self.embedding.encode(
            [prompt], convert_to_numpy=True)

        query_embedding = np.array(query_embedding).reshape(1, -1)

        similarities = cosine_similarity(query_embedding, embed_chunk)[0]

        top_k_indices = np.argsort(similarities)[-top_k:][::-1]

        relevant_chunks = [chunks[i] for i in top_k_indices]
        return relevant_chunks
