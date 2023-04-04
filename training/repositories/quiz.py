from training import models
from .base import BaseRepository


class QuizRepository(BaseRepository):
    __model__ = models.Quiz
