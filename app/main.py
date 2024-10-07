import socket  # noqa: F401

def create_nessage(param_id: int) -> bytes:
    # Convert the integer to a 4-byte big-endian byte array
    id_bytes = param_id.to_bytes(4, byteorder='big')
    header = len(id_bytes).to_bytes(4, byteorder='big')
    return  header + id_bytes

def handle_client(client: socket.socket):
    req = client.recv(1024) # read data from client
    correlation_id = int.from_bytes(req[8:12], byteorder='big')
    client.sendall(create_nessage(correlation_id)) # send data to client
    client.close()

def main():
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    while True:
        client, _ = server.accept() # wait for client
        handle_client(client)
        

if __name__ == "__main__":
    main()
