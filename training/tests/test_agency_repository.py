import pytest
from training import schemas, models
from training.repositories import AgencyRepository


def test_create(agency_repo_empty: AgencyRepository, valid_agency):
    result = agency_repo_empty.create(valid_agency)
    assert result.id
    assert result.name == valid_agency.name


def test_create_duplicate(agency_repo_with_data: AgencyRepository, valid_agency):
    with pytest.raises(Exception):
        agency_repo_with_data.create(valid_agency)


def test_find_by_name(agency_repo_with_data: AgencyRepository, valid_agency):
    result = agency_repo_with_data.find_by_name(valid_agency)
    assert result is not None
    assert result.name == valid_agency.name


def test_find_by_nonexistent_name(agency_repo_empty: AgencyRepository):
    invalid_agency = schemas.AgencyCreate(name="Nonexistent Agency", bureau=None)
    result = agency_repo_empty.find_by_name(invalid_agency)
    assert result is None


def test_save(agency_repo_empty: AgencyRepository, valid_agency):
    result = agency_repo_empty.save(models.Agency(name=valid_agency.name, bureau=valid_agency.bureau))
    assert result.id
    retrieved_result = agency_repo_empty.find_by_id(result.id)
    assert retrieved_result is not None
    assert retrieved_result.name == valid_agency.name and retrieved_result.bureau == valid_agency.bureau


def test_find_by_id(agency_repo_empty: AgencyRepository, valid_agency):
    agency_id = agency_repo_empty.save(models.Agency(name=valid_agency.name, bureau=valid_agency.bureau)).id
    result = agency_repo_empty.find_by_id(agency_id)
    assert result is not None
    assert result.name == valid_agency.name


def test_find_by_nonexistent_id(agency_repo_empty: AgencyRepository, valid_agency):
    agency_id = agency_repo_empty.save(models.Agency(name=valid_agency.name, bureau=valid_agency.bureau)).id
    result = agency_repo_empty.find_by_id(agency_id + 1)
    assert result is None


def test_find_all(agency_repo_with_data: AgencyRepository, testdata: dict):
    result = agency_repo_with_data.find_all()
    names = list(map(lambda r: r.name, result))
    bureaus = list(map(lambda r: r.bureau, result))
    for item in testdata["agencies"]:
        assert item["name"] in names and item["bureau"] in bureaus


def test_delete_by_id(agency_repo_empty: AgencyRepository, valid_agency):
    agency_id = agency_repo_empty.save(models.Agency(name=valid_agency.name, bureau=valid_agency.bureau)).id
    agency_repo_empty.delete_by_id(agency_id)
    assert agency_repo_empty.find_by_id(agency_id) is None
