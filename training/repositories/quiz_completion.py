from sqlalchemy.orm import Session
from training import models, schemas
from .base import BaseRepository


class QuizCompletionRepository(BaseRepository[models.QuizCompletion]):

    def __init__(self, session: Session):
        super().__init__(session, models.QuizCompletion)

    def create(self, quiz_completion: schemas.QuizCompletionCreate) -> models.QuizCompletion:
        return self.save(models.QuizCompletion(
            quiz_id=quiz_completion.quiz_id,
            user_id=quiz_completion.user_id,
            passed=quiz_completion.passed
        ))

    def get_certificate_by_id(self, id: int) -> models.QuizCompletion | None:
        return self._session.query(models.QuizCompletion).filter(models.QuizCompletion.id == id, models.QuizCompletion.passed).first()
