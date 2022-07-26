import json


class ConnectionHandler:
    """Connection hanlder for websockets"""

    def __init__(self, socket):
        self.socket = socket
        self.accept_request()

    async def accept_request(self):
        """Accepts connection"""
        self.socket.accept()

    async def get_request(self) -> dict:
        """Get Data in Request"""
        return await self.process_incoming_connection()

    async def send_response(self, response: dict):
        """Send Response to websocket"""
        await self.socket.send_text(json.dumps(response))

    async def process_incoming_connection(self) -> dict:
        """Process Incoming Connection and get request"""
        request = await self.socket.receive_text()
        return self.parse_request(request)

    def parse_request(self, request: str) -> dict:
        """Parse data from request string"""
        return json.loads(request)
