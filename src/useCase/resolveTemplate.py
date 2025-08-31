
import json
import re
from src.infraestructure.embedding import AiEmbedding
from src.infraestructure.semantic import AiSemantic
from src.application.dto import ApiResponse, ResolveDTO
from src.infraestructure.aiClient import AiClient
from src.infraestructure.mongo import MappingRepository


class ResolveTemplate:
    repository: MappingRepository
    aiClient: AiClient
    embedding: AiEmbedding
    semantic: AiSemantic

    def __init__(
            self,
            repository: MappingRepository,
            aiClient: AiClient,
            embedding: AiEmbedding,
            semantic: AiSemantic):
        self.repository = repository
        self.aiClient = aiClient
        self.embedding = embedding
        self.semantic = semantic

    def execute(self, dto: ResolveDTO) -> ApiResponse:

        mappings = self.repository.findAll()

        mappings_dict = [mapping.__str__() for mapping in mappings]

        entry = {
            "input": dto.input,
            "output": dto.output
        }

        information = f"""
        Dadas as informações de input e seu respectivo output, use seus conhecimentos para gerar um template handlebars válido para resolver o problema. Abaixo está o seu problema:

        problema:

        {entry}

        Importante: Retorne apenas o template para economizarmos tokens e processamento.
        """

        chunk_embedding = self.embedding.embed(mappings_dict)

        relevant_chunks = self.semantic.find_relevant_chunks(
            information, mappings_dict, chunk_embedding)

        augmented = self._augmented_retrieval(information, relevant_chunks)

        content = self.aiClient.send(
            "Você é um agente especializado em handlebars e tem acesso à documentação de handlebars existente https://handlebarsjs.com/guide/ . Use também possíveis documentos de treinamento para combinar seus conhecimentos. Sempre teste seu template usando o input para que o resultado seja exatamente igual ao output passado",
            augmented
        )

        final_json = self._normalize_json(content)

        return ApiResponse(
            statusCode=200,
            message="O template foi gerado com sucesso",
            template=final_json
        )

    def _normalize_json(
            self,
            json_puro: str
    ) -> str:

        clean_text = json_puro.strip()
        pattern_inicio = r'^```json\s*'
        prefix = re.sub(pattern_inicio, '', clean_text)
        sufix = r'```$'
        final = re.sub(sufix, '', prefix)
        return final.strip()

    def _augmented_retrieval(
            self,
            prompt,
            relevant_chunks
    ):
        context = "\n\n".join(relevant_chunks)
        augmented_prompt = f"""
        Use as informações do contexto abaixo para responder à pergunta.
        Se a resposta não estiver no contexto, use sua própria base de conhecimento.

        Contexto:
        ---
        {context}
        ---

        Pergunta: {prompt}
        """
        return augmented_prompt
