
from typing import Any


class MappingBusinessException(Exception):
    message: str
    statusCode: int

    def __init__(self, message: str):
        self.message = message
        self.statusCode = 400

    def __str__(self):
        return self.message


class AiClientAuthenticationException(Exception):
    message: str
    statusCode: int

    def __init__(self, message: str):
        self.message = message
        self.statusCode = 400

    def __str__(self):
        return self.message


class ErrorDecodingHandlebarsTemplateException(Exception):
    message: str
    statusCode: int

    def __init__(self, message: str):
        self.message = message
        self.statusCode = 500

    def __str__(self):
        return self.message


class TemplateReprocessingExceedRetriesException(Exception):
    message: str
    statusCode: int

    def __init__(self, message: str):
        self.message = message
        self.statusCode = 400

    def __str__(self):
        return self.message


class IncorrectHandlebarsTemplateException(Exception):
    message: str
    statusCode: int
    template: str
    desired_output: Any
    output_from_template: Any

    def __init__(self, message: str, template: str, output: Any, template_output: Any):
        self.message = message
        self.statusCode = 400
        self.template = template
        self.desired_output = output
        self.output_from_template = template_output

    def __str__(self):
        return self.message
