
from fastapi import Depends
from src.infraestructure.log.logAdapter import LogAdapter
from src.infraestructure.handlebars.handlebars import Handlebars
from src.infraestructure.ai.semantic import AiSemantic
from src.infraestructure.ai.aiClient import AiClient
from src.infraestructure.ai.embedding import AiEmbedding

from src.infraestructure.mongo.mongo import MappingRepository, ReportRepository
from src.useCase.mapExample import MapExample
from src.useCase.resolveTemplateAsync import ResolveTemplateAsync
from src.useCase.resolveTemplateSync import ResolveTemplateSync
from src.useCase.getTemplateString import GetTemplateString


def get_mappingRepository() -> MappingRepository:
    return MappingRepository()


def get_logAdapter() -> LogAdapter:
    return LogAdapter()


def get_reportRepository() -> ReportRepository:
    return ReportRepository()


def get_aiClient() -> AiClient:
    return AiClient()


def get_aiEmbedding() -> AiEmbedding:
    return AiEmbedding()


def get_aiSemantic() -> AiSemantic:
    return AiSemantic()


def get_Handlebars_validator() -> Handlebars:
    return Handlebars()


def get_mapExample_useCase(
    repo: MappingRepository = Depends(get_mappingRepository),
    log: LogAdapter = Depends(get_logAdapter)
) -> MapExample:
    return MapExample(repo, log)


def get_template_str_useCase(
    report_repo: ReportRepository = Depends(get_reportRepository)
) -> GetTemplateString:
    return GetTemplateString(report_repo)


def get_resolveTemplate_useCase(
    repo: MappingRepository = Depends(get_mappingRepository),
    report_repo: ReportRepository = Depends(get_reportRepository),
    aiClient: AiClient = Depends(get_aiClient),
    embedding: AiEmbedding = Depends(get_aiEmbedding),
    semantic: AiSemantic = Depends(get_aiSemantic),
    log: LogAdapter = Depends(get_logAdapter)
) -> ResolveTemplateSync:
    return ResolveTemplateSync(
        repo,
        report_repo,
        aiClient,
        embedding,
        semantic,
        log
    )


def get_resolveTemplateAsync_useCase(
    repo: MappingRepository = Depends(get_mappingRepository),
    report_repo: ReportRepository = Depends(get_reportRepository),
    aiClient: AiClient = Depends(get_aiClient),
    embedding: AiEmbedding = Depends(get_aiEmbedding),
    semantic: AiSemantic = Depends(get_aiSemantic),
    handlebars: Handlebars = Depends(get_Handlebars_validator),
    logAdapter: LogAdapter = Depends(get_logAdapter)
) -> ResolveTemplateSync:
    return ResolveTemplateAsync(
        repo,
        report_repo,
        aiClient,
        embedding,
        semantic,
        handlebars,
        logAdapter
    )
