from pydantic import BaseModel


class User(BaseModel):
    """User object model"""

    user_id: int
    name: str
    chatroom_id: str
