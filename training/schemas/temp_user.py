from pydantic import BaseModel, EmailStr


class TempUser(BaseModel):
    '''
    This class represents a user how has filled out the form to begin
    a quiz, but who's email has not been validated yet.
    '''
    email: EmailStr
    first_name: str
    last_name: str
    agency: str  # maybe an id?
