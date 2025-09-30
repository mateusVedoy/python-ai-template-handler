
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse

from src.dependencies import get_mapExample_useCase, get_resolveTemplate_useCase, get_resolveTemplateAsync_useCase, get_template_str_useCase
from src.application.dto import ApiResponse, MappingDTO, ResolveDTO
from src.domain.exception import MappingBusinessException
from src.useCase.mapExample import MapExample
from src.useCase.resolveTemplateAsync import ResolveTemplateAsync
from src.useCase.resolveTemplateSync import ResolveTemplateSync
from src.useCase.getTemplateString import GetTemplateString


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


@router.get("/async/{processing_template_id}", response_model=ApiResponse)
async def get_template_str_async(
    processing_template_id: str,
    get_template_str: GetTemplateString = Depends(get_template_str_useCase)
) -> ApiResponse:

    if not processing_template_id:
        raise HTTPException(
            status_code=400,
            detail="cannot get template without identifier processing")

    return get_template_str.get(processing_template_id)


# TER RECURSO PARA ADICIONAR FUNÇÕES DISPONÍVEIS PARA USAR NOS TEMPLATES
# neste caso preciso garantir que haverá explicação sobre o que a função faz
# e exemplos de como usá-la em templates
