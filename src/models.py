from datetime import datetime

from pydantic import BaseModel


class UserModel(BaseModel):
    """User object model"""

    name: str
    user_id: str
    chatroom_id: str


class MessageModel(BaseModel):
    """Message object model"""

    message_id: int
    body: str
    timestamp: datetime


class ChatRoomModel(BaseModel):
    """ChatRoom object model"""

    chatroom_id: str
    messages: list[MessageModel]
    user_id: str


# Response Models
class SignUpResponseModel(BaseModel):
    """Sign Up Response Model"""

    status: bool
    user: UserModel


class SendMessageResponseModel(BaseModel):
    """Send Message Response Model"""

    status: bool
    message: MessageModel


class ChatRoomResponseModel(BaseModel):
    """Get Messages Response Model"""

    chatroom_id: str
    messages: list[MessageModel]
