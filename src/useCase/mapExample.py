
from src.application.dto import ApiResponse, MappingDTO
from src.domain.mapping import Mapping
from src.infraestructure.mongo import MappingRepository

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

    def __init__(self, repository: MappingRepository):
        self.repository = repository

    def execute(
        self,
        example: MappingDTO
    ) -> ApiResponse:

        mapping = Mapping(
            example.alias,
            example.description,
            example.input,
            example.output,
            example.template
        )

        self.repository.save(mapping)

        return ApiResponse(
            statusCode=201,
            message="example template has been saved",
            template="")
