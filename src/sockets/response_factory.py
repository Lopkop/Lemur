from src.db.models.messages_model import ChatRoom
from src.models import UserModel, MessageModel, ChatRoomModel, SingUpResponseModel, SendMessageResponseModel


class ResponseFactory:
    def generate_sign_up_response(self, status: bool, user_model: UserModel) -> str:
        """Generates sign up response in JSON"""
        response_model = SingUpResponseModel(status=status, user=user_model)
        return response_model.json()

    def generate_send_message_response(self, status: bool, message: Message) -> str:
        """Generates send_message response in JSON"""
        message_model = MessageModel(message_id=message.id, body=message.body, timestamp=message.created_at)
        response_model = SendMessageResponseModel(status=status, message=message_model)
        return response_model.json()

    def generate_get_messages_response(self, chatroom: ChatRoom) -> str:
        """Generates get_messages response in JSON"""
        chatroom_model = ChatRoomModel(chatroom_id=chatroom.id, messages=chatroom.messages, user_id=chatroom.user_id)
        return chatroom_model.json(exclude={'user_id'})
