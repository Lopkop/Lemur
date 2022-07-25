from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from ..session import Base


class User(Base):
    """User Table Definition"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    chat_room_id = Column(String, unique=True)
    created_at = Column(Date)
    updated_at = Column(Date)

    children = relationship("messages")

    def __repr__(self):
        return "<User(name='{}', chat_room_id='{}')>".format(
            self.name, self.chat_room_id
        )
