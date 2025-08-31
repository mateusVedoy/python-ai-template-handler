
from fastapi import Depends
from src.infraestructure.semantic import AiSemantic
from src.infraestructure.embedding import AiEmbedding
from src.infraestructure.aiClient import AiClient
from src.infraestructure.mongo import MappingRepository
from src.useCase.mapExample import MapExample
from src.useCase.resolveTemplate import ResolveTemplate


def get_mappingRepository() -> MappingRepository:
    return MappingRepository()


def get_aiClient() -> AiClient:
    return AiClient()


def get_aiEmbedding() -> AiEmbedding:
    return AiEmbedding()


def get_aiSemantic() -> AiSemantic:
    return AiSemantic()


def get_mapExample_useCase(
    repo: MappingRepository = Depends(get_mappingRepository)
) -> MapExample:
    return MapExample(repo)


def get_resolveTemplate_useCase(
    repo: MappingRepository = Depends(get_mappingRepository),
    aiClient: AiClient = Depends(get_aiClient),
    embedding: AiEmbedding = Depends(get_aiEmbedding),
    semantic: AiSemantic = Depends(get_aiSemantic)
) -> ResolveTemplate:
    return ResolveTemplate(
        repo,
        aiClient,
        embedding,
        semantic
    )
