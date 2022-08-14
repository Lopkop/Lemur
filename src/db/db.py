from src.db.models import ChatRoom
from src.db.models import Message
from src.db.models import User
from src.db.session import Session
from src.schemas import ChatRoomModel, MessageModel, UserModel


class DatabaseService:
    """DB API service"""

    @staticmethod
    def save_user(user_model: UserModel) -> None:
        """Saves user object to database"""
        user = User(name=user_model.name)
        Session.add(user)
        Session.commit()

    def add_user_to_chatroom(self, user_model: UserModel, chatroom_model: ChatRoomModel):
        user = self.fetch_user_by_name(user_model.name)
        chat = self.fetch_chat_by_name(chatroom_model.name)
        user.chatroom = chat.name
        chat.users.append(user)
        Session.commit()

    def save_chatroom(self, chatroom_model: ChatRoomModel) -> None:
        user = self.fetch_user_by_name(chatroom_model.users[0].name)
        chatroom = ChatRoom(name=chatroom_model.name, users=[user])
        Session.add(chatroom)
        Session.commit()

    @staticmethod
    def save_message(chatroom_name: str, message_model: MessageModel) -> None:
        """Saves a message to the chatroom"""
        message = Message(
            chatroom=chatroom_name,
            user=message_model.user,
            text=message_model.text,
        )
        Session.add(message)
        Session.commit()

    @staticmethod
    def fetch_user_by_name(username: str) -> User:
        """Fetch User by username"""
        user = Session.query(User).filter_by(name=username).first()
        return user

    @staticmethod
    def fetch_chat_by_name(name: str) -> ChatRoom:
        chat = Session.query(ChatRoom).filter_by(name=name).first()
        return chat

    @staticmethod
    def get_chat_room_messages(chatroom_name: str, page: int = 1, size: int = 20):
        """Fetch all messages in a chat room"""
        page = page - 1
        offset = page * size
        messages = (
            Session.query(Message)
                .filter_by(chatroom=chatroom_name)
                .order_by(Message.created_at.desc())
                .limit(size)
                .offset(offset)
                .all()
        )
        return messages
