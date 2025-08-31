import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os


class AiSemantic:
    embedding: str
    task_type: str

    def __init__(self):
        self.embedding = os.getenv("GEMINI_EMBEDDING_MODEL")
        self.task_type = "retrieval_query"

    def find_relevant_chunks(self, prompt, chunks, embed_chunk, top_k=3) -> list:

        if len(chunks) == 0:
            return []

        query_embedding = genai.embed_content(
            model=self.embedding,
            content=prompt,
            task_type=self.task_type)['embedding']

        query_embedding = np.array(query_embedding).reshape(1, -1)

        similarities = cosine_similarity(query_embedding, embed_chunk)[0]

        top_k_indices = np.argsort(similarities)[-top_k:][::-1]

        relevant_chunks = [chunks[i] for i in top_k_indices]
        return relevant_chunks
