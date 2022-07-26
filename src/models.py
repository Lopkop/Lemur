from pydantic import BaseModel


class UserModel(BaseModel):
    """User object model"""

    name: str
    user_id: int
    name: str
    chatroom_id: str


class MessageModel(BaseModel):
    """Message object model"""

    message_id: int
    body: str
    timestamp: int  # todo: should be replaced (ex: datetime.datetime)


class ChatRoomModel(BaseModel):
    """ChatRoom object model"""

    chatroom_id: int
    messages: list[MessageModel]
    user_id: int


class SingUpResponseModel(BaseModel):
    status: bool
    user: UserModel


class SendMessageResponseModel(BaseModel):
    status: bool
    message: MessageModel
