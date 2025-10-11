
import pytest
from src.domain.exception import MappingBusinessException
from src.domain.mapping import Mapping


class TestMapping:

    def test_should_throw_error_when_input_is_incomplete(self):

        with pytest.raises(MappingBusinessException):
            Mapping(
                None,
                "description",
                "input",
                "output",
                "template"
            )

        with pytest.raises(MappingBusinessException):
            Mapping(
                "alias",
                None,
                "input",
                "output",
                "template"
            )

        with pytest.raises(MappingBusinessException):
            Mapping(
                "alias",
                "description",
                None,
                "output",
                "template"
            )

        with pytest.raises(MappingBusinessException):
            Mapping(
                "alias",
                "description",
                "input",
                None,
                "template"
            )

        with pytest.raises(MappingBusinessException):
            Mapping(
                "alias",
                "description",
                "input",
                "output",
                None
            )

    def test_validate_mapping_dict(self):

        mapping = Mapping(
            "123-alias",
            "description",
            {"prop": "value"},
            {"prop": {"data": "value"}},
            "{\"prop\": {\"data\": {{prop}} }}"
        )

        expected_dict = {
            "alias": "123-alias",
            "description": "description",
            "input": {"prop": "value"},
            "output": {"prop": {"data": "value"}},
            "template": "{\"prop\": {\"data\": {{prop}} }}"
        }

        assert expected_dict == mapping.to_dict()

    def test_should_stringify_mapping_dict(self):

        mapping = Mapping(
            "123-alias",
            "description",
            {"prop": "value"},
            {"prop": {"data": "value"}},
            "{\"prop\": {\"data\": {{prop}} }}"
        )

        expected_str = "{\"alias\": \"123-alias\", \"description\": \"description\", \"input\": {\"prop\": \"value\"}, \"output\": {\"prop\": {\"data\": \"value\"}}, \"template\": \"{\\\"prop\\\": {\\\"data\\\": {{prop}} }}\"}"

        assert expected_str == mapping.__str__()
