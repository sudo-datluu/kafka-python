import socket
import argparse
from time import sleep
from random import randint, choice

def send_request(
        client: socket.socket, 
        body: bytes=b"\x00\x12\x00\x04\xa6\xc7\xdc\xcb\x00\tkafka-cli\x00\nkafka-cli\x040.1\x00",
    ) -> bytes:

    header = (len(body)).to_bytes(4, byteorder='big')
    # Send the request to the server
    byte_stream = header + body
    print(f"Sending request: {byte_stream}")
    client.send(byte_stream)

    # Receive the response from the server
    response = client.recv(1024)

    return response

def main():
    parser = argparse.ArgumentParser(description="Kafka Client")
    parser.add_argument("--host", type=str, help="Server host", default="localhost")
    parser.add_argument("--port", type=int, help="Server port", default=9092)
    args = parser.parse_args()

    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client.connect((args.host, args.port))
    try:
        while True:
            body = input("Enter request body: ")
            body = body.encode() if body else None

            # Send request and get response
            response = send_request(client)

            # Print the response
            print("Received response:", response)

            # Optional: Sleep for a short duration before the next input
            sleep(1)
    except KeyboardInterrupt:
        print("\nClient terminated by user.")
    finally:
        # Close the connection
        client.close()

if __name__ == "__main__":
    main()