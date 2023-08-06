from threedi_cmd_statistics.validators.strings import validate_organisations
from threedi_cmd_statistics.validators import ValidationError
from uuid import uuid4
import pytest


@pytest.fixture
def organisations():
    organisations = []
    for i in range(5):
        u = uuid4().hex
        organisations.append(u)
    yield organisations


def test_organisations_validation(organisations):
    assert validate_organisations(organisations) is None


def test_invalid_organisations(organisations):
    organisations[0] += "4444"
    with pytest.raises(ValidationError):
        validate_organisations(organisations)


def test_all_option():
    organisations = ["all"]
    assert validate_organisations(organisations) is None
