import socket  # noqa: F401
from .utils import create_message
from .api import APIVersions

def handle_client(client: socket.socket):
    req = client.recv(1024) # read first 1024 bytes of data from client
    apiVersionObj = APIVersions(req)

    # Send the response back to the client
    client.sendall(apiVersionObj.to_bytes())

def main():
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    while True:
        client, address = server.accept() # wait for client
        print(f"Connection from {address}")
        handle_client(client)
        print(f"Connection from {address} closed")

if __name__ == "__main__":
    main()
