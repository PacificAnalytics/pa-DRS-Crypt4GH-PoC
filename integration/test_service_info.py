import pytest
import requests


@pytest.fixture
def api_endpoint():
    return "http://localhost:8080/ga4gh/drs/v1/service-info"


@pytest.fixture
def expected_response():
    return {
        "contactUrl": "contact/abc",
        "createdAt": "2020-01-01",
        "crypt4gh": {
            "pubkey": "AmEsb2n0m5mc6aadwpK4sT6zNapqgH+nnysNtpKa2Ag="
        },
        "description": "Description of service.",
        "documentationUrl": "docs/abc",
        "environment": "ENV",
        "id": "TEMPID1",
        "name": "TEMP_STUB",
        "organization": {
            "name": "Parent organization",
            "url": "parent/abc"
        },
        "type": {
            "artifact": "TEMP_ARTIFACT",
            "group": "TEMP_GROUP",
            "version": "v1"
        },
        "updatedAt": "2020-01-01",
        "version": "0.0.0"
    }


def test_get_service_info(api_endpoint, expected_response):
    response = requests.get(api_endpoint)

    assert response.status_code == 200
    assert response.json() == expected_response
