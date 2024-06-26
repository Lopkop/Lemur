from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[dict] = {}

    async def connect(self, chatroom, username, websocket: WebSocket):
        await websocket.accept()
        try:
            self.active_connections[chatroom][username] = websocket
        except KeyError:
            self.active_connections[chatroom] = {username: websocket}

    def disconnect(self, chatroom, username):
        del self.active_connections[chatroom][username]

    async def send_message(self, chatroom, message):
        for websocket in self.active_connections[chatroom].values():
            await websocket.send_text(message)
