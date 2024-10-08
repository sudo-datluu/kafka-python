import asyncio
from .messages.request import KafkaRequest
from .messages.response import KafkaResponse

class KafkaServer:
    async def start(self) -> None:
        print("[STARTING] Server starting...")
        server = await asyncio.start_server(
            self._handle_client, "localhost", 9092, reuse_port=True
        )
        print(f"[LISTENING] Server started on {server.sockets[0].getsockname()}")
        async with server:
            await server.serve_forever()

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        while True:
            try:
                request = await KafkaRequest.from_stream_reader(reader)
            except asyncio.IncompleteReadError:
                break

            response = KafkaResponse.from_request(request)
            print(response)
            writer.write(response.encode())
            await writer.drain()

        writer.close()
        await writer.wait_closed()