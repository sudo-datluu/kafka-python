import socket

def send_request():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9092))
    
    # Define the header values
    apikey = (18).to_bytes(2, byteorder='big') # Example 8-byte API key
    apiversion = (43).to_bytes(2, byteorder='big')  # Example API version as a 4-byte integer
    correlationid = (1234).to_bytes(4, byteorder='big')  # Example correlation id as a 4-byte integer
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
    send_request()
