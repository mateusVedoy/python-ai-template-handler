import json
from typing import Any

from src.domain.exception import MappingBusinessException


class Mapping:
    """
    Representa um mapeamento a ser usado pela IA para resolver templates
    """
    alias: str
    description: str
    input: Any
    output: Any
    template: str

    def __init__(self, alias: str, description: str, input: Any, output: Any, template: str):
        self.alias = alias
        self.description = description
        self.input = input
        self.output = output
        self.template = template
        self._validate()

    def _validate(self):
        if self.alias is None:
            raise MappingBusinessException(
                "O campo 'alias' não deve estar nulo")
        if self.description is None:
            raise MappingBusinessException(
                "O campo 'description' não deve estar nulo")
        if self.input is None:
            raise MappingBusinessException(
                "O campo 'input' não deve estar nulo")
        if self.output is None:
            raise MappingBusinessException(
                "O campo 'output' não deve estar nulo")
        if self.template is None:
            raise MappingBusinessException(
                "O campo 'template' não deve estar nulo")

    def to_dict(self):
        return {
            "alias": self.alias,
            "description": self.description,
            "input": self.input,
            "output": self.output,
            "template": self.template
        }

    def to_json_string(self, indent: int = None) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def __str__(self) -> str:
        return self.to_json_string()

    def __repr__(self) -> str:
        return f"Mapping(alias='{self.alias}')"
