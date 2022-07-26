from pydantic import BaseModel
from datetime import datetime

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
    user_id: int


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

    chatroom_id: int
    messages: list[MessageModel]