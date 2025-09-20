
import uuid
from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.responses import JSONResponse

from src.dependencies import get_mapExample_useCase, get_resolveTemplate_useCase, get_resolveTemplateAsync_useCase
from src.application.dto import ApiResponse, MappingDTO, ResolveDTO
from src.domain.exception import MappingBusinessException
from src.useCase.mapExample import MapExample
from src.useCase.resolveTemplateAsync import ResolveTemplateAsync
from src.useCase.resolveTemplateSync import ResolveTemplateSync


router = APIRouter(prefix="/template", tags=["router"])


@router.post("/example", response_model=ApiResponse)
async def add_template(
    example: MappingDTO,
    map_example: MapExample = Depends(get_mapExample_useCase)
) -> ApiResponse:

    return map_example.execute(example)


@router.post("/resolve", response_model=ApiResponse)
async def resolve_template(
    template: ResolveDTO,
    resolve_template: ResolveTemplateSync = Depends(
        get_resolveTemplate_useCase)
) -> ApiResponse:

    processingId = str(uuid.uuid4())
    return resolve_template.execute(processingId, template)


@router.post("/resolve/async", status_code=status.HTTP_202_ACCEPTED)
async def resolve_async_template(
    template: ResolveDTO,
    background_tasks: BackgroundTasks,
    resolve_async_template: ResolveTemplateAsync = Depends(
        get_resolveTemplateAsync_useCase)
) -> ApiResponse:

    try:

        processingId = str(uuid.uuid4())

        background_tasks.add_task(
            resolve_async_template.execute, template, processingId)

        return JSONResponse(
            status_code=202,
            content={
                "statusCode": 202,
                "message": "Processing started. You can check the result in a few minutes",
                "processingId": processingId,
                "_links": {
                    "report": f"/report/{processingId}"
                }
            }
        )

    except MappingBusinessException as e:
        print(e)
    except Exception as e:
        print(e)

# TER RECURSO PARA ADICIONAR FUNÇÕES DISPONÍVEIS PARA USAR NOS TEMPLATES
# neste caso preciso garantir que haverá explicação sobre o que a função faz
# e exemplos de como usá-la em templates
