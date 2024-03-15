from pydantic import BaseModel

from db.schemas import MessageModel, ChatRoomModel


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


class ChatRequest(BaseModel):
    chatname: str
    username: str
