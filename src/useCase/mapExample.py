
import time
from src.infraestructure.log.logAdapter import LogAdapter
from src.application.dto import ApiResponse, MappingDTO
from src.domain.mapping import Mapping
from src.infraestructure.mongo.mongo import MappingRepository

#
# entender se salva embedding da descrição tbm na base
# para facilitar a busca dos dados relacionados à busca
#
# na v1 avmos buscar todo e qualquer template salvo de exemplo
# para treinar o modelo
#
# mais além vou precisar entender como filtramos as buscas do mongo de acordo
# com o tipo de template e conversão para não trazer tudo
#
# talvez precise enviar para o modelo de IA gerar sua descrição e essa seja salva no banco
# para usarmos posteriormente para buscar
#


class MapExample:

    repository: MappingRepository
    logAdapter: LogAdapter

    def __init__(self, repository: MappingRepository, logAdapter: LogAdapter):
        self.repository = repository
        self.logAdapter = logAdapter

    def execute(
        self,
        example: MappingDTO
    ) -> ApiResponse:

        try:

            start = time.perf_counter()

            mapping = Mapping(
                example.alias,
                example.description,
                example.input,
                example.output,
                example.template
            )

            self.repository.save(mapping)

            self.logAdapter.template_example_generated(
                example.alias,
                "example of template has been generated",
                self._generateProcessingTime(start)
            )

            return ApiResponse(
                statusCode=201,
                message="example template has been saved",
                template="")

        except Exception as e:

            self.logAdapter.template_example_generation_error(
                example.alias, e.__str__(), self._generateProcessingTime(start))

            return ApiResponse(
                statusCode=400,
                message=e.__str__(),
                template=""
            )

    def _generateProcessingTime(self, start_processing: float) -> float:
        end_processing = time.perf_counter()
        return end_processing - start_processing
