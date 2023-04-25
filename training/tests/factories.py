from polyfactory.factories.pydantic_factory import ModelFactory
from training import schemas


class QuizGradeSchemaFactory(ModelFactory[schemas.QuizGrade]):
    __model__ = schemas.QuizGrade


class QuizCompletionFactory(ModelFactory[schemas.QuizCompletion]):
    __model__ = schemas.QuizCompletion


class QuizCreateSchemaFactory(ModelFactory[schemas.QuizCreate]):
    __model__ = schemas.QuizCreate


class QuizSchemaFactory(ModelFactory[schemas.Quiz]):
    __model__ = schemas.Quiz


class QuizSubmissionSchemaFactory(ModelFactory[schemas.QuizSubmission]):
    __model__ = schemas.QuizSubmission


class UserSchemaFactory(ModelFactory[schemas.User]):
    __model__ = schemas.User


class UserCreateSchemaFactory(ModelFactory[schemas.UserCreate]):
    __model__ = schemas.UserCreate


class AgencySchemaFactory(ModelFactory[schemas.Agency]):
    __model__ = schemas.Agency


class AgencyCreateSchemaFactory(ModelFactory[schemas.AgencyCreate]):
    __model__ = schemas.AgencyCreate
