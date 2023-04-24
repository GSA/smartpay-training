from fastapi.testclient import TestClient
from fastapi import status
from training.main import app
from training.repositories import AgencyRepository
from training.tests.factories import AgencyCreateSchemaFactory, AgencySchemaFactory


client = TestClient(app)


def test_create_agency(mock_agency_repo: AgencyRepository):
    agency_create = AgencyCreateSchemaFactory.build()
    mock_agency_repo.find_by_name.return_value = None
    mock_agency_repo.create.return_value = AgencySchemaFactory.build()
    response = client.post(
        "/api/v1/agencies",
        json=agency_create.dict()
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_agency_duplicate(mock_agency_repo: AgencyRepository):
    agency_create = AgencyCreateSchemaFactory.build()
    agency = AgencySchemaFactory.build(name=agency_create.name)
    mock_agency_repo.find_by_name.return_value = agency
    response = client.post(
        "/api/v1/agencies",
        json=agency_create.dict()
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_agencies_all(mock_agency_repo: AgencyRepository):
    agencies = [AgencySchemaFactory.build() for x in range(3)]
    mock_agency_repo.find_all.return_value = agencies
    response = client.get(
        "/api/v1/agencies"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3


def test_get_agency(mock_agency_repo: AgencyRepository):
    agency = AgencySchemaFactory.build()
    mock_agency_repo.find_by_id.return_value = agency
    response = client.get(
        "/api/v1/agencies/2"
    )
    assert response.status_code == status.HTTP_200_OK


def test_get_agency_invalid_id(mock_agency_repo: AgencyRepository):
    mock_agency_repo.find_by_id.return_value = None
    response = client.get(
        "/api/v1/agencies/2"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
