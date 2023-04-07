from typing import Generic, Optional, List, Type, TypeVar
from sqlalchemy.orm import Session
from training import models


T = TypeVar("T", bound=models.Base)


class BaseRepository(Generic[T]):

    def __init__(self, session: Session, model: Type[T]):
        self._session = session
        self._model = model

    def save(self, item: T) -> T:
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def find_by_id(self, id: int) -> Optional[T]:
        return self._session.query(self._model).filter(
            self._model.id == id  # type: ignore
        ).first()

    def find_all(self) -> List[T]:
        return self._session.query(self._model).all()

    def delete_by_id(self, id: int) -> None:
        self._session.query(self._model).filter(
            self._model.id == id  # type: ignore
        ).delete()
