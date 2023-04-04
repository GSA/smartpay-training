from collections.abc import Generator
from fastapi import Depends
from training.repositories import AgencyRepository, UserRepository, QuizRepository
from training.database import SessionLocal
from sqlalchemy.orm import Session


def db() -> Generator[Session, None, None]:
    '''
    Provides a database session that automatically rolls back upon an
    Exception.
    '''
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


def agency_repository(db: Session = Depends(db)) -> AgencyRepository:
    return AgencyRepository(db)


def user_repository(db: Session = Depends(db)) -> UserRepository:
    return UserRepository(db)


def quiz_repository(db: Session = Depends(db)) -> QuizRepository:
    return QuizRepository(db)
