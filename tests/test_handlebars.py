import pytest
from src.domain.exception import IncorrectHandlebarsTemplateException
from src.application.dto import ResolveDTO
from src.infraestructure.handlebars.handlebars import Handlebars


class TestHandlebars:
    """
    Classe de teste para a validação de templates Handlebars.
    """

    def test_validate_handlebars_with_success(self):
        """
        Cenário 1: Valida um template Handlebars que é compilado e
        gera a saída esperada corretamente.
        """

        handlebars = Handlebars()
        template = '{"message": "Hello, {{name}}!"}'
        template_input = {"name": "World"}
        expected_output = {"message": "Hello, World!"}

        try:
            handlebars.validate(template, template_input, expected_output)
            validation_passed = True
        except Exception:
            validation_passed = False

        assert validation_passed, "A validação falhou em alguma exception lançada"

    def test_should_validate_template_with_error(self):
        """Testa o cenário de falha com uma saída incorreta."""

        handlebars = Handlebars()

        template = '{"message": "Hello, {{name}}!"}'
        template_input = {"name": "World"}

        dto = ResolveDTO(
            description="Converte dados...",
            input=template_input,
            output={
                "personal_information": {"name": "John", "age": 30},
                "location": {
                    "city": {"name": "London"},
                    "zipcode": {"code": "10001"}
                }
            }
        )

        with pytest.raises(IncorrectHandlebarsTemplateException):
            handlebars.validate(
                template=template,
                input=dto.input,
                output=dto.output
            )
