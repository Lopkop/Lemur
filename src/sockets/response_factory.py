from src.db.models.messages_model import ChatRoom
from src.models import UserModel, MessageModel, ChatRoomModel, ChatRoomResponseModel, SignUpResponseModel, SendMessageResponseModel


class ResponseFactory:
    def generate_sign_up_response(self, status: bool, user_model: UserModel) -> str:
        """Generates sign up response in JSON"""
        response_model = SignUpResponseModel(status=status, user=user_model)
        return response_model.json()

    def generate_send_message_response(self, status: bool, message: MessageModel) -> str:
        """Generates send_message response in JSON"""
        response_model = SendMessageResponseModel(status=status, message=message_model)
        return response_model.json()

    def generate_get_messages_response(self, chatroom: ChatRoomModel) -> str:
        """Generates get_messages response in JSON"""
        chatroom_model = ChatRoomResponseModel(chatroom)
        return chatroom_model.json()
