import socket
import argparse

def send_request(api_key: int, api_version: int, correlation_id: int):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9092))
    
    # Define the header values
    apikey = (api_key).to_bytes(2, byteorder='big', signed=True) # Example 8-byte API key
    apiversion = (api_version).to_bytes(2, byteorder='big')  # Example API version as a 4-byte integer
    correlationid = (correlation_id).to_bytes(4, byteorder='big', signed=True)  # Example correlation id as a 4-byte integer
    clientid = "clientid"  # Example 8-byte client ID
    
    # Construct the message (headers + any body you want to send)
    message = apikey + apiversion + correlationid + clientid.encode('utf-8')
    
    header = (len(message)).to_bytes(4, byteorder='big')

    # Send the message to the server
    client.sendall(header + message)
    
    # Wait for the response from the server
    response = client.recv(1024)
    print(f"Response from server: {response}")
    
    client.close()

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--api_key", type=int, help="API Key", default=18)
    args.add_argument("--api_version", type=int, help="API Version", default=4)
    args.add_argument("--correlation_id", type=int, help="Correlation ID", default=1234)
    send_request(**vars(args.parse_args()))
