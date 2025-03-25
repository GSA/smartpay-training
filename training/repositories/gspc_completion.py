from sqlalchemy.orm import Session
from training import models, schemas
from .base import BaseRepository


class GspcCompletionRepository(BaseRepository[models.GspcCompletion]):

    def __init__(self, session: Session):
        super().__init__(session, models.GspcCompletion)

    def create(self, gspc_completion: schemas.GspcCompletion) -> models.GspcCompletion:
        return self.save(models.GspcCompletion(
            user_id=gspc_completion.user_id,
            passed=gspc_completion.passed,
            certification_expiration_date=gspc_completion.certification_expiration_date,
            responses=gspc_completion.responses,
            gspc_invite_id=gspc_completion.gspc_invite_id
        ))
