"""Initial

Revision ID: ac79b6bd39ba
Revises: 
Create Date: 2024-05-02 14:46:35.589419

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

# revision identifiers, used by Alembic.
from db.models import Message

revision: str = 'ac79b6bd39ba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('Message',
                    Column('id', Integer, primary_key=True),
                    Column('text', Text),
                    Column('created_at', DateTime, server_default=func.now()),
                    Column('chatroom', String, ForeignKey("chatrooms.name")),
                    Column('user', String, ForeignKey("users.name"))
                    )
    op.create_table('UserChatRoom',
                    Column('id', Integer, primary_key=True),
                    Column('chatroom', String, ForeignKey("chatrooms.name")),
                    Column('user', String, ForeignKey("users.name"))
                    )
    op.create_table('ChatRoom',
                    Column('id', Integer, primary_key=True),
                    Column('name', String, unique=True),
                    )
    op.create_table('User',
                    Column('id', Integer, primary_key=True),
                    Column('name', String, unique=True),
                    Column('hashed_password', String),
                    Column('lifetime', DateTime)
                    )
    op.create_table('Token',
                    Column('id', Integer, primary_key=True),
                    Column('token', String, unique=True),
                    Column('expires_at', DateTime),
                    )

    def downgrade() -> None:
        # ### commands auto generated by Alembic - please adjust! ###
        pass
        # ### end Alembic commands ###
