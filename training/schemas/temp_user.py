from pydantic import BaseModel, EmailStr


class TempUser(BaseModel):
    '''
    This class represents a user how has filled out the form to begin
    a quiz, but who's email has not been validated yet.
    '''
    email: EmailStr
    name: str
    agency: str  # maybe an id?
    page_id: str


class IncompleteTempUser(BaseModel):
    '''
    This class represents a user that may or not be known yet.
    '''
    email: EmailStr
    page_id: str
