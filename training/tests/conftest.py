import pytest
from training.database import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event


@pytest.fixture(scope="function")
def db():
    '''
    This fixture initiates a transactional DB session and rolls back all
    changes after the test case completes.

    This essentially replaces training.database.get_db in the tests.
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
