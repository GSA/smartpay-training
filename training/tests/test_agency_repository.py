import pytest
from training import schemas, models
from training.repositories import AgencyRepository


def test_create(agency_repo: AgencyRepository, valid_agency_name):
    result = agency_repo.create(schemas.AgencyCreate(name=valid_agency_name))
    assert result.id
    assert result.name == valid_agency_name


def test_create_duplicate(agency_repo_with_data: AgencyRepository, valid_agency_name):
    with pytest.raises(Exception):
        agency_repo_with_data.create(schemas.AgencyCreate(name=valid_agency_name))


def test_find_by_name(agency_repo_with_data: AgencyRepository, valid_agency_name):
    result = agency_repo_with_data.find_by_name(valid_agency_name)
    assert result.name == valid_agency_name


def test_find_by_nonexistent_name(agency_repo: AgencyRepository):
    result = agency_repo.find_by_name("Nonexistent Agency")
    assert result is None


def test_save(agency_repo: AgencyRepository, valid_agency_name):
    result = agency_repo.save(models.Agency(name=valid_agency_name))
    assert result.id
    assert agency_repo.find_by_id(result.id).name == valid_agency_name


def test_find_by_id(agency_repo: AgencyRepository, valid_agency_name):
    agency_id = agency_repo.save(models.Agency(name=valid_agency_name)).id
    result = agency_repo.find_by_id(agency_id)
    assert result.name == valid_agency_name


def test_find_by_nonexistent_id(agency_repo: AgencyRepository, valid_agency_name):
    agency_id = agency_repo.save(models.Agency(name=valid_agency_name)).id
    result = agency_repo.find_by_id(agency_id + 1)
    assert result is None


def test_find_all(agency_repo_with_data: AgencyRepository, valid_agency_names):
    result = agency_repo_with_data.find_all()
    names = list(map(lambda r: r.name, result))
    for name in valid_agency_names:
        assert name in names


def test_delete_by_id(agency_repo: AgencyRepository, valid_agency_name):
    agency_id = agency_repo.save(models.Agency(name=valid_agency_name)).id
    agency_repo.delete_by_id(agency_id)
    assert agency_repo.find_by_id(agency_id) is None
