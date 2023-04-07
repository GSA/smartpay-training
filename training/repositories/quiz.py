from sqlalchemy.orm import Session
from training import models, schemas
from .base import BaseRepository


class QuizRepository(BaseRepository[models.Quiz]):

    def __init__(self, session: Session):
        super().__init__(session, models.Quiz)

    def create(self, quiz: schemas.QuizCreate) -> models.Quiz:
        content_dict = quiz.content.dict()
        for qindex, question in enumerate(content_dict.get("questions", [])):
            question["id"] = qindex
            for cindex, choice in enumerate(question.get("choices", [])):
                choice["id"] = cindex

        new_quiz = self.save(models.Quiz(
            name=quiz.name,
            topic=quiz.topic,
            audience=quiz.audience,
            active=quiz.active,
            content=content_dict,
        ))

        return new_quiz
