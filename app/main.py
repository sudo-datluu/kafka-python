import socket  # noqa: F401
from .utils import create_message
from .api import APIVersions

def handle_client(client: socket.socket):
    req = client.recv(2048)
    apiVersionObj = APIVersions(req)

    # Send the response back to the client
    client.sendall(apiVersionObj.to_bytes())
    print(f"Close request from correlation id:  {apiVersionObj.kafka_request.correlation_id}")

def main():
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    client, address = server.accept() # wait for client
    print(f"Connection from {address}")
    while True:
        handle_client(client)

if __name__ == "__main__":
    main()
