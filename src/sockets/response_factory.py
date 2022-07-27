from src.models import (
    ChatRoomModel,
    ChatRoomResponseModel,
    MessageModel,
    SendMessageResponseModel,
    SignUpResponseModel,
    UserModel,
)


class ResponseFactory:
    def generate_sign_up_response(status: bool, user_model: UserModel) -> dict:
        """Generates sign up response in JSON"""
        response_model = SignUpResponseModel(status=status, user=user_model)
        return response_model.dict()

    def generate_send_message_response(status: bool, message: MessageModel) -> dict:
        """Generates send_message response in JSON"""
        response_model = SendMessageResponseModel(status=status, message=message)
        return response_model.dict()

    def generate_get_messages_response(chatroom: ChatRoomModel) -> dict:
        """Generates get_messages response in JSON"""
        chatroom_model = ChatRoomResponseModel(chatroom)
        return chatroom_model.dict()
