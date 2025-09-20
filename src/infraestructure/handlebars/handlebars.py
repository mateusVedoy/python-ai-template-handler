import json
from typing import Any, Dict
import pybars

from src.domain.exception import ErrorDecodingHandlebarsTemplateException, IncorrectHandlebarsTemplateException


class Handlebars:

    def __init__(self):
        self.compiler = pybars.Compiler()

    # retorna exception quando não bate
    def validate(self, template: str, input: Dict[str, Any], output: Dict[str, Any]) -> bool:

        try:
            compiled_template = self.compiler.compile(template)
            actual_output_str = compiled_template(input)

            try:
                actual_data = json.loads(actual_output_str)

                if isinstance(output, dict):
                    self.validate_as_dict(template, actual_data, output)
                else:
                    expected_data = json.loads(str(output))
                    self.validate_as_dict(template, expected_data, output)

            except (json.JSONDecodeError, TypeError):

                raise ErrorDecodingHandlebarsTemplateException(
                    "error deconding handlebars template")

            except IncorrectHandlebarsTemplateException as e:
                raise e

        except IncorrectHandlebarsTemplateException as e:
            raise e

        except Exception as e:
            raise ErrorDecodingHandlebarsTemplateException(e.args)

    def validate_as_dict(self, template: str, replaced_json: Any, output: Dict[str, Any]):
        if (not replaced_json == output):
            raise IncorrectHandlebarsTemplateException(
                message="Handlebars template is incorrect",
                template=template,
                output=output,
                template_output=replaced_json
            )
