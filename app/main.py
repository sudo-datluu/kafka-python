import socket  # noqa: F401
from .api import APIVersions
from threading import Thread, active_count

def handle_client(client: socket.socket, address: str):
    print(f"[NEW CONNECTION] Got connection from {address}")
    while True:
        req = client.recv(1024)
        apiVersionObj = APIVersions(req)
        # Send the response back to the client
        client.send(apiVersionObj.to_bytes())

def main():
    print("[STARTING] Server starting...")
    server = socket.create_server(("localhost", 9092), reuse_port=True)
    print(f"[LISTENING] Server started on {server.getsockname()}")
    while True:
        client, address = server.accept() # wait for client
        thread = Thread(target=handle_client, args=(client, address))
        thread.start()
        print(f"[INFO] Active connections: {active_count() - 1}")


if __name__ == "__main__":
    main()
