class ResponseFactory:
    def generate_sign_up_response(outcome: bool, user: User):
        """Generates sign up response JSON"""
        return {
            "outcome": outcome,
            "user": {
                "user_name": username,
                "user_id": user.user_id,
                "chatroom_id": user.chatroom_id,
            },
        }

    def generate_send_message_response(outcome: bool, message: Message):
        """Generates send_message response JSON"""
        return {
            "status": outcome,
            "message": {
                "chatroom_id": message.chatroom_id,
                "timestamp": message.timestamp,
                "message": message.body,
            },
        }

    def generate_get_messages_response(chatroom: Chatroom):
        """Generates get_messages response JSON"""
        return {"chatroom_id": chatroom.id, "messages": chatroom.messages}
