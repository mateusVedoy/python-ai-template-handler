from typing import Any, Dict
from pydantic import BaseModel


class ApiResponse(BaseModel):
    statusCode: int
    message: str
    template: str


class MappingDTO(BaseModel):
    """
    DTO para treinar api com exemplos de conversão de entrada para saída com template definido
    """
    alias: str
    description: str
    input: Dict[str, Any]
    output: Dict[str, Any]
    template: str


class ResolveDTO(BaseModel):
    """
    DTO com o qual o usuário informa qual entrada (input) e qual saída esperada (output) para gerarmos o template
    """
    description: str
    input: Dict[str, Any]
    output: Dict[str, Any]
