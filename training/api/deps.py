from fastapi import Depends
from training.repositories import AgencyRepository, UserRepository
from training.database import SessionLocal
from sqlalchemy.orm import Session


def db() -> None:
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
