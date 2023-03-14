from typing import List
import pytest
from training import schemas, models
from training.repositories.agency import AgencyRepository
from sqlalchemy.orm import Session


@pytest.fixture
def valid_names() -> List[str]:
    return [
        "Department of Mysteries",
        "Department of Magical Law Enforcement",
        "Department of Magical Accidents and Catastrophes",
    ]


@pytest.fixture
def valid_name(valid_names: List[str]) -> str:
    return valid_names[0]


@pytest.fixture
def db_with_data(db: Session, valid_names: List[str]):
    for name in valid_names:
        db.add(models.Agency(name=name))
    db.commit()
    yield db


@pytest.fixture
def repo(db: Session) -> AgencyRepository:
    yield AgencyRepository(session=db)


@pytest.fixture
def repo_with_data(db_with_data: Session) -> AgencyRepository:
    yield AgencyRepository(session=db_with_data)


def test_create(repo: AgencyRepository, valid_name):
    result = repo.create(schemas.AgencyCreate(name=valid_name))
    assert result.id
    assert result.name == valid_name


def test_create_duplicate(repo_with_data: AgencyRepository, valid_name):
    with pytest.raises(Exception):
        repo_with_data.create(schemas.AgencyCreate(name=valid_name))


def test_find_by_name(repo_with_data: AgencyRepository, valid_name):
    result = repo_with_data.find_by_name(valid_name)
    assert result.name == valid_name


def test_find_by_nonexistent_name(repo: AgencyRepository):
    result = repo.find_by_name("Nonexistent Agency")
    assert result is None


def test_save(repo: AgencyRepository, valid_name):
    result = repo.save(models.Agency(name=valid_name))
    assert result.id
    assert repo.find_by_id(result.id).name == valid_name


def test_find_by_id(repo: AgencyRepository, valid_name):
    agency_id = repo.save(models.Agency(name=valid_name)).id
    result = repo.find_by_id(agency_id)
    assert result.name == valid_name


def test_find_by_nonexistent_id(repo: AgencyRepository, valid_name):
    agency_id = repo.save(models.Agency(name=valid_name)).id
    result = repo.find_by_id(agency_id + 1)
    assert result is None


def test_find_all(repo_with_data: AgencyRepository, valid_names):
    result = repo_with_data.find_all()
    names = list(map(lambda r: r.name, result))
    for name in valid_names:
        assert name in names


def test_delete_by_id(repo: AgencyRepository, valid_name):
    agency_id = repo.save(models.Agency(name=valid_name)).id
    repo.delete_by_id(agency_id)
    assert repo.find_by_id(agency_id) is None
