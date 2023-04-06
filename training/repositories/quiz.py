from training import models, schemas
from .base import BaseRepository


class QuizRepository(BaseRepository):
    __model__ = models.Quiz

    def create(self, quiz: schemas.QuizCreate) -> schemas.Quiz:
        content_dict = quiz.content.dict()
        for qindex, question in enumerate(content_dict.get("questions", [])):
            question["id"] = qindex
            for cindex, choice in enumerate(question.get("choices", [])):
                choice["id"] = cindex

        db_quiz = self.save(models.Quiz(
            name=quiz.name,
            topic=quiz.topic,
            audience=quiz.audience,
            active=quiz.active,
            content=content_dict,
        ))

        return schemas.Quiz.from_orm(db_quiz)

    def find_by_id(self, id: int) -> schemas.Quiz | None:
        db_quiz = self._session.query(self.__model__).filter(self.__model__.id == id).first()
        if db_quiz is None:
            return None
        return schemas.Quiz.from_orm(db_quiz)
