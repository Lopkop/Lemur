from pydantic import BaseModel


class User(BaseModel):
    """User object model"""

    username: str
    user_id: int
    chatroom_id: str
