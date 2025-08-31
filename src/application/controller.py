
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.dependencies import get_mapExample_useCase, get_resolveTemplate_useCase
from src.application.dto import ApiResponse, MappingDTO, ResolveDTO
from src.domain.exception import MappingBusinessException
from src.useCase.mapExample import MapExample
from src.useCase.resolveTemplate import ResolveTemplate


router = APIRouter(prefix="/template", tags=["router"])


@router.post("/example", response_model=ApiResponse)
async def add_template(
    example: MappingDTO,
    map_example: MapExample = Depends(get_mapExample_useCase)
) -> ApiResponse:

    try:

        return map_example.execute(example)

    except MappingBusinessException as e:
        return JSONResponse(
            status_code=e.statusCode,
            content={
                "statusCode": e.statusCode,
                "message": str(e)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "statusCode": 500,
                "message": str(e)
            }
        )


@router.post("/resolve", response_model=ApiResponse)
async def resolve_template(
    template: ResolveDTO,
    resolve_template: ResolveTemplate = Depends(get_resolveTemplate_useCase)
) -> ApiResponse:

    try:

        return resolve_template.execute(template)

    except MappingBusinessException as e:
        return JSONResponse(
            status_code=e.statusCode,
            content={
                "statusCode": e.statusCode,
                "message": str(e)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "statusCode": 500,
                "message": str(e)
            }
        )

# TER RECURSO PARA ADICIONAR FUNÇÕES DISPONÍVEIS PARA USAR NOS TEMPLATES
    # neste caso preciso garantir que haverá explicação sobre o que a função faz
    # e exemplos de como usá-la em templates
