from pydantic import BaseModel


class UserModel(BaseModel):
    """User object model"""

    name: str


class MessageModel(BaseModel):
    """Message object model"""

    user: str
    text: str


class ChatRoomModel(BaseModel):
    """ChatRoom object model"""

    name: str
    messages: list[MessageModel]
    users: list[UserModel]


# Response Models
class SignUpResponseModel(BaseModel):
    """Sign Up Response Model"""

    status: bool
    user: UserModel


class SendMessageResponseModel(BaseModel):
    """Send Message Response Model"""

    status: bool
    message: MessageModel


class GetMessagesResponseModel(BaseModel):
    """Get Messages Response Model"""

    status: bool
    name: str
    messages: list[MessageModel]


class CreateChatResponseModel(ChatRoomModel):
    """Create Chatroom Response Model"""

    status: bool
