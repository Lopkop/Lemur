from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect
from sqlalchemy.orm import scoped_session
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware  # todo: later should be replaced

from sockets.connection_manager import ConnectionManager
from db.dbapi import DatabaseService
from db.schemas import MessageModel
from sockets.response_factory import ResponseFactory

from auth.api import auth_router
from chatroom.api import chat_router

app = FastAPI()
db = DatabaseService()
response_factory = ResponseFactory()
manager = ConnectionManager()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)


@app.websocket('/{chatroom}/{username}')
async def websocket_endpoint(
        websocket: WebSocket,
        username: str,
        chatroom: str,
        session: scoped_session = Depends(db.get_db)):
    await manager.connect(chatroom, username, websocket)

    try:
        while True:
            text = await websocket.receive_text()
            message = MessageModel(text=text, user=username)
            db.save_message(session, chatroom, message)

            await manager.send_message(chatroom, message.json())
            print(f'{username} sent "{text}" to {chatroom}')  # need to log, not print

    except WebSocketDisconnect:
        manager.disconnect(chatroom, username)
