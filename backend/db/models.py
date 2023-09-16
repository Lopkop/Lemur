from .database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship


class Message(Base):
    """Message Table Definition"""

    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    chatroom = Column(String, ForeignKey("chatrooms.name"))
    user = Column(String, ForeignKey("users.name"))

    def __repr__(self):
        return f"<Message(user='{self.user}', chatroom='{self.chatroom}', text='{self.text}')>"


class User(Base):
    """User Table Definition"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    chatroom = Column(String, ForeignKey("chatrooms.name"))
    messages = relationship(Message)

    def __repr__(self):
        return f"<User(name='{self.name}', chatroom='{self.chatroom}', messages='{self.messages}')>"


class ChatRoom(Base):
    """Message Table Definition"""

    __tablename__ = "chatrooms"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    users = relationship(User)
    messages = relationship(Message)

    def __repr__(self):
        return f"<ChatRoom(chatroom_name='{self.name}', users='{self.users}', messages='{self.messages}')>"
