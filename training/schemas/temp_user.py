from pydantic import ConfigDict, BaseModel, EmailStr, field_validator


class TempUser(BaseModel):
    '''
    This class represents a user how has filled out the form to begin
    a quiz, but who's email has not been validated yet.
    '''
    email: EmailStr
    name: str
    agency_id: int
    model_config = ConfigDict(from_attributes=True)

    @field_validator("agency_id", mode="before")
    @classmethod
    def to_int(cls, value: str | int) -> int:
        '''
            This addresses a bug in pydantic that does not correctly choose
            the right value from the union[TempUser, IncompleteTempUser]
            when agency_id is a string. Related:
            https://docs.pydantic.dev/dev-v2/migration/#unions
        '''
        if isinstance(value, str):
            value = int(value)

        return value


class IncompleteTempUser(BaseModel):
    '''
    This class represents a user that may or not be known yet.
    '''
    email: EmailStr


class WebDestination(BaseModel):
    '''
    This class allow the front-end to communicate
    the destination the user should be taken
    after the loginless flow completes
    '''
    page_id: str
    parameters: str
    title: str
