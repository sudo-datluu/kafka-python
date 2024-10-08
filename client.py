import socket
import argparse
from time import sleep
from random import randint

def send_request(client: socket, api_key: int, api_version: int):
    # Define the header values
    apikey = (api_key).to_bytes(2, byteorder='big', signed=True) # Example 8-byte API key
    apiversion = (api_version).to_bytes(2, byteorder='big')  # Example API version as a 4-byte integer

    # correlation_id = randint(0, 999999999)
    correlation_id = randint(-999999999, 999999999)
    correlationid = (correlation_id).to_bytes(4, byteorder='big', signed=True)  # Example correlation id as a 4-byte integer
    clientid = "clientid"  # Example 8-byte client ID
    print(f"Sending request with correlation id: {correlation_id}")

    # Construct the message (headers + any body you want to send)
    message = apikey + apiversion + correlationid + b"\x00" + clientid.encode('utf-8')
    
    header = (len(message)).to_bytes(4, byteorder='big')
    client.send(header + message)    
    # Wait for the response from the server
    response = client.recv(1024)
    print(f"Response from server: {response}")


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--api_key", type=int, help="API Key", default=18)
    args.add_argument("--api_version", type=int, help="API Version", default=4)
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9092))

    for i in range(10):
        send_request(client=client, **vars(args.parse_args()))
        sleep(1)
    client.close()