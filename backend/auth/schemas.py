from pydantic import BaseModel


class AuthResponseModel(BaseModel):
    status: int
    token_expires_at: float
