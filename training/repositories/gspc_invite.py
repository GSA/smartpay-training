from sqlalchemy.orm import Session
from training import models
from datetime import datetime
from .base import BaseRepository


class GspcInviteRepository(BaseRepository[models.GspcInvite]):

    def __init__(self, session: Session):
        super().__init__(session, models.GspcInvite)

    def create(self, email: str, certification_expiration_date: datetime) -> models.GspcInvite:
        return self.save(models.GspcInvite(
            email=email,
            certification_expiration_date=certification_expiration_date
        ))
