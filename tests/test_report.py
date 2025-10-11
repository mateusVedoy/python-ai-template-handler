
from src.domain.report import Report


class TestReport:

    def test_should_create_report_and_validate_props(self):
        """
        Valida a criação de entidade report com seus dados
        """

        report = Report(
            "123-identifier",
            123,
            "COMPLETED",
            "template criado com sucesso",
            "{\"prop\": \"val\"}"
        )

        report_dict = report.to_dict()

        expected_dict = {
            "identifier": "123-identifier",
            "processingTime": 123,
            "template":  "{\"prop\": \"val\"}",
            "status": "COMPLETED",
            "message": "template criado com sucesso"
        }

        assert report_dict == expected_dict
