from typing import Any, Generic, Optional, List, Type, TypeVar
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
        return self._session.query(self._model).filter_by(id=id).first()

    def find_all(self, filters: dict[str, Any] = {}) -> List[T]:
        query = self._session.query(self._model)
        for key, value in filters.items():
            query = query.filter(getattr(self._model, key) == value)
        return query.all()

    def delete_by_id(self, id: int) -> None:
        self._session.query(self._model).filter_by(id=id).delete()
