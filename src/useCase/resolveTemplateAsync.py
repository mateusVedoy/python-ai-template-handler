import time
from typing import Any
from src.infraestructure.log.logAdapter import LogAdapter
from src.infraestructure.ai.aiClient import AiClient
from src.infraestructure.ai.embedding import AiEmbedding
from src.infraestructure.ai.semantic import AiSemantic
from src.domain.exception import IncorrectHandlebarsTemplateException, TemplateReprocessingExceedRetriesException
from src.application.dto import ResolveDTO
from src.infraestructure.handlebars.handlebars import Handlebars
from src.infraestructure.mongo.mongo import MappingRepository, ReportRepository
from src.useCase.resolveTemplate import ResolveTemplate


class ResolveTemplateAsync(ResolveTemplate):
    mapping_repository: MappingRepository
    aiClient: AiClient
    embedding: AiEmbedding
    semantic: AiSemantic
    validador: Handlebars
    logAdapter: LogAdapter

    def __init__(
            self,
            mapping_repository: MappingRepository,
            report_repository: ReportRepository,
            aiClient: AiClient,
            embedding: AiEmbedding,
            semantic: AiSemantic,
            handlebars: Handlebars,
            logAdapter: LogAdapter):
        super().__init__(report_repository)
        self.mapping_repository = mapping_repository
        self.report_repository = report_repository
        self.aiClient = aiClient
        self.embedding = embedding
        self.semantic = semantic
        self.validador = handlebars
        self.logAdapter = logAdapter

    def execute(self, dto: ResolveDTO, processing_id: str) -> None:

        self.logAdapter.starting_resolve_template(
            processing_id,
            "resolve template async has been started")

        start = time.perf_counter()

        mappings = self.mapping_repository.findAll()

        mappings_dict = [mapping.__str__() for mapping in mappings]

        information = super().set_information(dto)

        chunk_embedding = self.embedding.embed(mappings_dict)

        relevant_chunks = self.semantic.find_relevant_chunks(
            information, mappings_dict, chunk_embedding)

        augmented = super()._augmented_retrieval(information, relevant_chunks)

        instruction = super().set_prompt_instruction()

        try:

            self.process(dto, instruction, augmented, processing_id, start)

        except IncorrectHandlebarsTemplateException as e:

            self.reprocess(e, instruction, relevant_chunks,
                           dto, start, processing_id)

        except Exception as e:
            self.logAdapter.template_generation_async_aborted(
                super()._generateProcessingTime(start),
                processing_id,
                e.__str__()
            )
            self._generateReport(
                processing_id, start, "PROCESS_ABORTED", e.__str__(), "")

    def set_reprocess_information(
            self,
            template: str,
            template_output: Any,
            desired_output: Any
    ) -> str:

        return f"""
        O template que você gerou anteriormente está incorreto de alguma forma. Preciso que você reveja o template, a saída geradoa a partir do template bem como a saída desejada. Compare a saída gerada pelo template com a saída desejada para realizar os ajustes necessários no template.

        template:
        {template}

        saída gerada com uso do template:
        {template_output}

        saída desejada:
        {desired_output}


        OBS: SEMPRE retorne APENAS o template ajustado. NÃO responda nada além do template, pois do contrário você quebrará o processo de minha aplicação.
        """

    def reprocess(
            self,
            exception: IncorrectHandlebarsTemplateException,
            instruction: str,
            relevant_chunk: list,
            dto: ResolveDTO,
            start_processing: float,
            processingId: str,
            retries=0) -> None:

        try:

            self.logAdapter.starting_reprocessing_template(
                processingId, retries, "reprocessing template new attempt started")

            if (retries > 2):
                raise TemplateReprocessingExceedRetriesException(
                    "max retries exceeded. Template processing aborted")

            retries += 1

            self.logAdapter.resolve_template_async_retry(
                processingId, f"Reprocessando template. Tentativa número {retries}")

            reprocess_information = self.set_reprocess_information(
                exception.template, exception.output_from_template, exception.desired_output)

            augmented = super()._augmented_retrieval(reprocess_information, relevant_chunk)

            content = self.aiClient.send(
                instruction,
                augmented
            )

            final_template = super()._normalize_json(content)

            self.validador.validate(final_template, dto.input, dto.output)

            self.logAdapter.template_compiled_successfully_async(
                super()._generateProcessingTime(start_processing),
                processingId,
                f"Template gerado com sucesso após {retries} tentativas\n\n"
            )

            self._generateReport(
                processingId, start_processing,
                "TEMPLATE_COMPILED_SUCCESSFULLY",
                f"Template foi gerado com sucesso após {retries} retentativas",
                final_template)

        except IncorrectHandlebarsTemplateException as e:

            self.reprocess(e, instruction, relevant_chunk,
                           dto, start_processing, processingId)

        except TemplateReprocessingExceedRetriesException as e:

            self._generateReport(processingId, start_processing, "RETRIES_EXCEEDED",
                                 e.__str__(), "")

        except Exception as e:
            self.logAdapter.template_generation_async_aborted(
                super()._generateProcessingTime(start_processing),
                processingId,
                e.__str__()
            )
            self._generateReport(processingId, start_processing, "PROCESS_ABORTED",
                                 e.__str__(), "")

    def process(self, dto: ResolveDTO, instruction: str, augmented: str, processing_id: str, start_processing: float) -> None:

        self.logAdapter.starting_processing_template(
            processing_id, "template processing attempt started")

        content = self.aiClient.send(
            instruction,
            augmented
        )

        final_template = super()._normalize_json(content)

        self.validador.validate(final_template, dto.input, dto.output)

        self.logAdapter.finish_resolve_template(
            processing_id,
            "resolve template sync has been finished")

        self.logAdapter.template_compiled_successfully_async(
            super()._generateProcessingTime(start_processing),
            processing_id,
            "Template generated successfully without retry"
        )

        self._generateReport(
            processing_id,
            start_processing,
            "TEMPLATE_COMPILED_SUCCESSFULLY",
            "template handlebars foi gerado com sucesso sem necessidade de reprocessamentos",
            final_template)

        self.logAdapter.report_compiled_successfully(
            processing_id, "report compilado com sucesso",  super()._generateProcessingTime(start_processing))
