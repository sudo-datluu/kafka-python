import socket  # noqa: F401
from .utils import create_message
from .api import Header

def handle_client(client: socket.socket):
    req = client.recv(1024) # read first 1024 bytes of data from client
    header = Header(req)
    print(header)
    error = None if header.isAllowed() else 35
    client.sendall(create_message(param_id=header.correlation_id, error=error)) # send data to client
    client.close()

def main():
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    while True:
        client, _ = server.accept() # wait for client
        handle_client(client)

if __name__ == "__main__":
    main()
