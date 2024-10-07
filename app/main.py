import socket  # noqa: F401

def create_nessage(param_id: int) -> bytes:
    # Convert the integer to a 4-byte big-endian byte array
    id_bytes = param_id.to_bytes(4, byteorder='big')

    return len(id_bytes).to_bytes(4, byteorder='big') + id_bytes

def main():
    print("Logs from your program will appear here!")

    server = socket.create_server(("localhost", 9092), reuse_port=True)
    while True:
        client, address = server.accept() # wait for client
        client.recv(1024) # read data from client
        client.sendall(create_nessage(7))
        client.close()

if __name__ == "__main__":
    main()
