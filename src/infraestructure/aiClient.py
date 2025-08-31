import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv
import numpy as np

from src.domain.exception import AiClientAuthenticationException
from src.domain.mapping import Mapping


class AiClient:
    model: str
    embedding: str
    apiKey: str

    def __init__(self):
        load_dotenv()
        self.model = os.getenv("GEMINI_MODEL")
        self.embedding = os.getenv("GEMINI_EMBEDDING_MODEL")
        self.apiKey = os.getenv("GEMINI_API_KEY")
        self._validate()

    def _validate(self):

        if not self.apiKey:
            raise AiClientAuthenticationException("ai api key cannot be unset")

        if not self.model:
            raise AiClientAuthenticationException("ai model cannot be unset")

        if not self.embedding:
            raise AiClientAuthenticationException(
                "ai embedding cannot be unset")

    def send(self, instruction, augmented_prompt):

        model = genai.GenerativeModel(model_name=self.model)

        initial_instruction = f"""{instruction}"""

        chat = model.start_chat(history=[{
            "role": "user",
            "parts": [initial_instruction]
        }])

        response_model = chat.send_message(augmented_prompt)

        return response_model.text

    def _define_augmented_prompt(self, user_prompt, relevant_chunks) -> str:

        context = "\n\n".join(relevant_chunks)
        augmented_prompt = f"""
        Use as informações do contexto abaixo para responder à pergunta.
        Se a resposta não estiver no contexto, use sua própria base de conhecimento.

        Contexto:
        ---
        {context}
        ---

        Pergunta: {user_prompt}
        """
        return augmented_prompt

    def _find_relevant_chunks(self, query, chunks, chunk_embeddings, top_k=2) -> list:
        """Encontra os chunks mais relevantes para a consulta"""

        if len(chunks) == 0:
            return []

        query_embedding = genai.embed_content(
            model=self.embedding,
            content=query,
            task_type="retrieval_query"
        )['embedding']

        query_embedding = np.array(query_embedding).reshape(1, -1)

        similarities = cosine_similarity(query_embedding, chunk_embeddings)[0]

        top_k_indices = np.argsort(similarities)[-top_k:][::-1]

        relevant_chunks = [chunks[i] for i in top_k_indices]
        return relevant_chunks

    def _embed_chunks(self, chunks: list[Mapping], embedding_model: str):

        if len(chunks) == 0:
            return np.array([])

        embedding = genai.embed_content(
            model=embedding_model,
            content=chunks,
            task_type="retrieval_document"
        )['embedding']

        return embedding
