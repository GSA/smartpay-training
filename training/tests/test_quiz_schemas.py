import pytest
from pydantic import ValidationError
from training import schemas


def test_create_invalid_topic(valid_quiz_create: schemas.QuizCreate):
    with pytest.raises(ValidationError):
        schemas.QuizCreate(
            name=valid_quiz_create.name,
            topic="Nonexistent",  # type: ignore
            audience=valid_quiz_create.audience,
            active=valid_quiz_create.active,
            content=valid_quiz_create.content
        )


def test_create_invalid_audience(valid_quiz_create: schemas.QuizCreate):
    with pytest.raises(ValidationError):
        schemas.QuizCreate(
            name=valid_quiz_create.name,
            topic=valid_quiz_create.topic,
            audience="Nonexistent",  # type: ignore
            active=valid_quiz_create.active,
            content=valid_quiz_create.content
        )
