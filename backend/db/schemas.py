from pydantic import BaseModel


class UserModel(BaseModel):
    """User object model"""

    name: str
    password: str
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
    messages: list[MessageModel]
    users: list[str]


# Response Models

class SignUpResponseModel(BaseModel):
    """Sign Up Response Model"""

    status: int
    access_token: str


class SendMessageResponseModel(BaseModel):
    """Send Message Response Model"""

    status: bool
    message: MessageModel


class GetMessagesResponseModel(BaseModel):
    """Get Messages Response Model"""

    status: bool
    name: str
    messages: list[MessageModel]


class ChatResponseModel(ChatRoomModel):
    """Chatroom Response Model"""

    status: int


class UserUndefinedModel(BaseModel):
    name: str
    status: int


class Token(BaseModel):
    access_token: str
    token_type: str


class ChatRequest(BaseModel):
    chatname: str
    username: str
