import pytest
from training import schemas, models
from training.repositories import AgencyRepository


def test_create(agency_repo_empty: AgencyRepository, valid_agency_name):
    result = agency_repo_empty.create(schemas.AgencyCreate(name=valid_agency_name))
    assert result.id
    assert result.name == valid_agency_name


def test_create_duplicate(agency_repo_with_data: AgencyRepository, valid_agency_name):
    with pytest.raises(Exception):
        agency_repo_with_data.create(schemas.AgencyCreate(name=valid_agency_name))


def test_find_by_name(agency_repo_with_data: AgencyRepository, valid_agency_name):
    result = agency_repo_with_data.find_by_name(valid_agency_name)
    assert result is not None
    assert result.name == valid_agency_name


def test_find_by_nonexistent_name(agency_repo_empty: AgencyRepository):
    result = agency_repo_empty.find_by_name("Nonexistent Agency")
    assert result is None


def test_save(agency_repo_empty: AgencyRepository, valid_agency_name):
    result = agency_repo_empty.save(models.Agency(name=valid_agency_name))
    assert result.id
    retrieved_result = agency_repo_empty.find_by_id(result.id)
    assert retrieved_result is not None
    assert retrieved_result.name == valid_agency_name


def test_find_by_id(agency_repo_empty: AgencyRepository, valid_agency_name):
    agency_id = agency_repo_empty.save(models.Agency(name=valid_agency_name)).id
    result = agency_repo_empty.find_by_id(agency_id)
    assert result is not None
    assert result.name == valid_agency_name


def test_find_by_nonexistent_id(agency_repo_empty: AgencyRepository, valid_agency_name):
    agency_id = agency_repo_empty.save(models.Agency(name=valid_agency_name)).id
    result = agency_repo_empty.find_by_id(agency_id + 1)
    assert result is None


def test_find_all(agency_repo_with_data: AgencyRepository, testdata: dict):
    result = agency_repo_with_data.find_all()
    names = list(map(lambda r: r.name, result))
    for name in testdata["agencies"]:
        assert name in names


def test_delete_by_id(agency_repo_empty: AgencyRepository, valid_agency_name):
    agency_id = agency_repo_empty.save(models.Agency(name=valid_agency_name)).id
    agency_repo_empty.delete_by_id(agency_id)
    assert agency_repo_empty.find_by_id(agency_id) is None
