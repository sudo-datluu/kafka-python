import socket
import argparse
from time import sleep
from random import randint
import dataclasses

def send_request(client: socket, api_key: int, api_version: int):
    # Define the header values
    apikey = (api_key).to_bytes(2, byteorder='big', signed=True) # Example 8-byte API key
    apiversion = (api_version).to_bytes(2, byteorder='big', signed=True)  # Example API version as a 4-byte integer

    # correlation_id = randint(0, 999999999)
    correlation_id = randint(-999999999, 999999999)
    correlationid = (correlation_id).to_bytes(4, byteorder='big', signed=True)  # Example correlation id as a 4-byte integer
    clientid = "clientid"  # Example 8-byte client ID
    print(f"Sending request with correlation id: {correlation_id}")

    tagged_fields = b"\x00"  # Example tagged fields
    # Construct the message (headers + any body you want to send)
    message = (apikey + 
        apiversion + 
        correlationid + 
        len(clientid).to_bytes(2) +
        clientid.encode('utf-8') +
        tagged_fields)
    
    header = (len(message)).to_bytes(4, byteorder='big')
    client.send(header + message)    
    # Wait for the response from the server
    response = client.recv(1024)
    print(f"Response from server: {response}")


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--api_key", type=int, help="API Key", default=18)
    args.add_argument("--api_version", type=int, help="API Version", default=4)
    
    template = {
        ""
    }

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9092))

    # for i in range(1):
    #     send_request(client=client, **vars(args.parse_args()))
    #     sleep(1)
    test = b'\x00\x00\x00#\x00\x12\x00\x045%Yk\x00\tkafka-cli\x00\nkafka-cli\x040.1\x00'
    
    client.send(test)
    res = client.recv(1024)
    client.close()