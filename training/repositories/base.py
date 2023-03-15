from typing import Optional, List
from sqlalchemy.orm import Session
from training import models


class BaseRepository:
    __model__ = models.Base

    def __init__(self, session: Session):
        self._session = session

    def save(self, item: __model__) -> __model__:
        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)
        return item

    def find_by_id(self, id: int) -> Optional[__model__]:
        return self._session.query(self.__model__).filter(self.__model__.id == id).first()

    def find_all(self) -> List[__model__]:
        return self._session.query(self.__model__).all()

    def delete_by_id(self, id: int) -> None:
        self._session.query(self.__model__).filter(self.__model__.id == id).delete()
