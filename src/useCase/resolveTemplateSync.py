import time
from src.infraestructure.log.logAdapter import LogAdapter
from src.infraestructure.ai.aiClient import AiClient
from src.infraestructure.ai.embedding import AiEmbedding
from src.infraestructure.ai.semantic import AiSemantic
from src.application.dto import ApiResponse, ResolveDTO
from src.infraestructure.mongo.mongo import MappingRepository, ReportRepository
from src.useCase.resolveTemplate import ResolveTemplate


class ResolveTemplateSync(ResolveTemplate):
    repository: MappingRepository
    aiClient: AiClient
    embedding: AiEmbedding
    semantic: AiSemantic
    logAdapter: LogAdapter

    def __init__(
            self,
            repository: MappingRepository,
            report_repository: ReportRepository,
            aiClient: AiClient,
            embedding: AiEmbedding,
            semantic: AiSemantic,
            logadApter: LogAdapter):
        super().__init__(report_repository)
        self.repository = repository
        self.aiClient = aiClient
        self.embedding = embedding
        self.semantic = semantic
        self.logAdapter = logadApter

    def execute(self, processingId: str, dto: ResolveDTO) -> ApiResponse:

        try:

            self.logAdapter.starting_resolve_template(
                processingId,
                "resolve template sync has been started")

            start = time.perf_counter()

            mappings = self.repository.findAll()

            mappings_dict = [mapping.__str__() for mapping in mappings]

            information = super().set_information(dto)

            chunk_embedding = self.embedding.embed(mappings_dict)

            relevant_chunks = self.semantic.find_relevant_chunks(
                information, mappings_dict, chunk_embedding)

            augmented = super()._augmented_retrieval(information, relevant_chunks)

            instruction = super().set_prompt_instruction()

            content = self.aiClient.send(
                instruction,
                augmented
            )

            final_json = super()._normalize_json(content)

            self.logAdapter.finish_resolve_template(
                processingId,
                "resolve template sync has been finished")

            self.logAdapter.template_compiled_successfully_sync(
                super()._generateProcessingTime(start),
                processingId,
                "template generated sync successfully"
            )

            return ApiResponse(
                statusCode=200,
                message="O template foi gerado com sucesso",
                template=final_json
            )

        except Exception as e:
            self.logAdapter.template_generation_sync_error(
                super()._generateProcessingTime(start),
                e.__str__(),
                ""
            )

            return ApiResponse(
                statusCode=400,
                message=e.__str__(),
                template=""
            )
