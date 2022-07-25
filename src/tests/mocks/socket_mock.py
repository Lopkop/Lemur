import asyncio


class SocketMock:
    def __init__(
            self,
            test_request: str = None,
    ):
        self.test_request = test_request

    async def accept(self):
        await asyncio.sleep(0.1)
        self.connection_accepted = True

    async def receive_text(self):
        await asyncio.sleep(0.1)
        return self.test_request

    async def send_text(self, message: str):
        await asyncio.sleep(0.1)
        self.sent_response = message
