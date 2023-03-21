from typing import List
import pytest
from training.database import engine
from training import models
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import event
from training.repositories import AgencyRepository


@pytest.fixture(scope="function")
def db():
    '''
    This fixture initiates a transactional DB session and rolls back all
    changes after the test case completes.
    '''

    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False)
    session = SessionLocal(bind=connection)
    session.begin_nested()
    already_rolled_back = False

    @event.listens_for(session, "after_rollback")
    def mark_rolled_back(_):
        '''
        The DB session is designed to rollback upon an exception, so no need to
        repeat a rollback if one has already been performed.
        '''
        nonlocal already_rolled_back
        already_rolled_back = True

    yield session

    session.close()
    if not already_rolled_back:
        transaction.rollback()
    connection.close()


@pytest.fixture
def valid_agency_names() -> List[str]:
    '''
    Provides a list of valid agency names.
    '''
    return [
        "Department of Mysteries",
        "Department of Magical Law Enforcement",
        "Department of Magical Accidents and Catastrophes",
    ]


@pytest.fixture
def valid_agency_name(valid_agency_names: List[str]) -> str:
    '''
    Provides a valid agency name.
    '''
    return valid_agency_names[0]


@pytest.fixture
def db_with_data(db: Session, valid_agency_names: List[str]):
    '''
    Provides a populated database.
    '''
    for name in valid_agency_names:
        db.add(models.Agency(name=name))
    db.commit()
    yield db


@pytest.fixture
def agency_repo(db: Session) -> AgencyRepository:
    '''
    Provides an AgencyRepository injected with an empty database.
    '''
    yield AgencyRepository(session=db)


@pytest.fixture
def agency_repo_with_data(db_with_data: Session) -> AgencyRepository:
    '''
    Provides an AgencyRepository injected with a populated database.
    '''
    yield AgencyRepository(session=db_with_data)
