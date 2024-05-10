from pydantic import BaseModel


class GspcResult(BaseModel):
    passed: bool
    cert_id: int
