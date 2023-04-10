from collections.abc import Generator
import os
import pytest
import yaml
import pathlib
from training.database import engine
from training import models
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import event
from training.repositories import AgencyRepository, UserRepository, QuizRepository


def pytest_generate_tests(metafunc):
    os.environ["DB_URI"] = "postgres://postgres:postgres@localhost:5432/smartpay-test"


@pytest.fixture
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
def db_with_data(db: Session, testdata: dict):
    '''
    Provides a fully populated database.
    '''

    agency_ids = []
    for name in testdata["agencies"]:
        agency = models.Agency(name=name)
        db.add(agency)
        db.commit()
        db.refresh(agency)
        agency_ids.append(agency.id)

    for index, user in enumerate(testdata["users"]):
        db.add(models.User(
            email=user["email"],
            name=user["name"],
            agency_id=agency_ids[index % 2]
        ))
        db.commit()

    for index, quiz in enumerate(testdata["quizzes"]):
        db.add(models.Quiz(
            name=quiz["name"],
            topic=quiz["topic"],
            audience=quiz["audience"],
            active=quiz["active"],
            content=quiz["content"]
        ))
        db.commit()

    yield db


@pytest.fixture
def testdata() -> dict:
    '''
    Provides a dictionary of test values from testdata.yaml. These values are
    loaded into the test database in the db_with_data fixture.
    '''
    datafile_path = pathlib.PurePath(pathlib.Path(__file__).parent.resolve(), "testdata.yaml")
    with open(datafile_path) as f:
        return yaml.safe_load(f)


@pytest.fixture
def valid_user_ids(db_with_data: Session) -> Generator[list[int], None, None]:
    '''
    Provides a list of user IDs that have been loaded into the test database.
    '''
    users = db_with_data.query(models.User).all()
    user_ids = list(map(lambda user: user.id, users))
    yield user_ids


@pytest.fixture
def valid_quiz_ids(db_with_data: Session) -> Generator[list[int], None, None]:
    '''
    Provides a list of quiz IDs that have been loaded into the test database.
    '''
    quizzes = db_with_data.query(models.Quiz).all()
    quiz_ids = list(map(lambda quiz: quiz.id, quizzes))
    yield quiz_ids


@pytest.fixture
def valid_agency_name(testdata: dict) -> Generator[str, None, None]:
    '''
    Provides a valid agency name.
    '''
    yield testdata["agencies"][0]


@pytest.fixture
def valid_user(testdata: dict) -> Generator[dict, None, None]:
    '''
    Provides a dict containing valid user values.
    '''
    yield testdata["users"][0]


@pytest.fixture
def agency_repo_empty(db: Session) -> Generator[AgencyRepository, None, None]:
    '''
    Provides an AgencyRepository injected with an empty database.
    '''
    yield AgencyRepository(session=db)


@pytest.fixture
def agency_repo_with_data(db_with_data: Session) -> Generator[AgencyRepository, None, None]:
    '''
    Provides an AgencyRepository injected with a populated database.
    '''
    yield AgencyRepository(session=db_with_data)


@pytest.fixture
def user_repo_empty(db: Session) -> Generator[UserRepository, None, None]:
    '''
    Provides an UserRepository injected with an empty database.
    '''
    yield UserRepository(session=db)


@pytest.fixture
def user_repo_with_data(db_with_data: Session) -> Generator[UserRepository, None, None]:
    '''
    Provides an UserRepository injected with a populated database.
    '''
    yield UserRepository(session=db_with_data)


@pytest.fixture
def quiz_repo_empty(db: Session) -> Generator[QuizRepository, None, None]:
    '''
    Provides a QuizRepository injected with an empty database.
    '''
    yield QuizRepository(session=db)


@pytest.fixture
def quiz_repo_with_data(db_with_data: Session) -> Generator[QuizRepository, None, None]:
    '''
    Provides a QuizRepository injected with a populated database.
    '''
    yield QuizRepository(session=db_with_data)
