class ConnectionHandler:
    def __init__(self, socket):
        self.socket = socket

    async def get_request(self) -> str:
        """Returns json request from client"""
        return await self.process_incoming_connection()

    async def send_response(self, response: str) -> None:
        """Sends json response to the client"""
        await self.socket.send_text(response)

    async def process_incoming_connection(self) -> str:
        """Accepts connection and returns request"""
        await self.socket.accept()
        request = await self.socket.receive_text()
        return request
