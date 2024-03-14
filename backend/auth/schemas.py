from pydantic import BaseModel


class AuthResponseModel(BaseModel):
    status: int
    access_token: str
    token_expires_at: float
