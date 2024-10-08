from kafka.server import KafkaServer
import asyncio
import time

if __name__ == "__main__":
    try:
        server = KafkaServer()
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\n[STOPPING] Server stopping...")
        # time.sleep(2)
        print("[STOPPED] Server stopped. Goodbye from dllt!")
