from pydantic import BaseModel


class UserModel(BaseModel):
    """User object model"""

    name: str
    password: str | None
    lifetime: int


class TokenModel(BaseModel):
    """Token object model"""

    access_token: str
    expires_at: int


class MessageModel(BaseModel):
    """Message object model"""

    user: str
    text: str


class ChatRoomModel(BaseModel):
    """ChatRoom object model"""

    name: str


class UserChatRoom(BaseModel):
    chatroom_name: str
    user: str
