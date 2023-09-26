from fastapi.testclient import TestClient
from fastapi import status
from training.main import app
from training.repositories import AgencyRepository
from training.schemas.agency import Bureau
from training.tests.factories import AgencySchemaFactory


client = TestClient(app)


def test_get_agencies_all(mock_agency_repo: AgencyRepository):
    agencies = [AgencySchemaFactory.build() for x in range(3)]
    parent_agencies = [record for record in agencies if record.bureau is None]
    transform_angecies = []
    for record in parent_agencies:
        agency_with_bureaus = [obj for obj in agencies if obj.bureau and obj.name == record.name]
        bureaus = []
        if len(agency_with_bureaus) > 0:
            for obj in agency_with_bureaus:
                bureau = Bureau(id=obj.id, name=obj.bureau)
                bureaus.append(bureau)

        transform_angecies.append({
                'id': record.id,
                'name': record.name,
                'bureaus': bureaus
        })
    mock_agency_repo.get_agencies_with_bureaus.return_value = transform_angecies
    response = client.get(
        "/api/v1/agencies"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(transform_angecies)


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
