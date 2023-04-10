from pydantic import BaseModel, EmailStr


class TempUser(BaseModel):
    '''
    This class represents a user how has filled out the form to begin
    a quiz, but who's email has not been validated yet.
    '''
    email: EmailStr
    name: str
    agency_id: int  # maybe an id?

    class Config:
        orm_mode = True


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
    title: str
