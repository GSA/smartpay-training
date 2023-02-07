from pydantic import BaseModel


class TempUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    agency: str  # maybe an id?
