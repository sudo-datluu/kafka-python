class Header:
    def __init__(self, req: bytes, size: int=1024):
        if len(req) > size:
            raise ValueError("Invalid header request size")
        
        # Extract the API key from the request
        self.api_key = int.from_bytes(req[4:6], byteorder='big') 

        # Extract the API version from the reques
        self.api_version = int.from_bytes(req[6:8], byteorder='big')

        # Extract the correlation ID from the request
        self.correlation_id = int.from_bytes(req[8:12], byteorder='big')

        # Extract the client ID from the request
        self.client_id = None

        self.size = size
    
    def isAllowed(self) -> bool:
        return self.api_key in [0, 1, 2, 3, 4]
    
    def __str__(self):
        return f"API Key: {self.api_key}, API Version: {self.api_version}, Correlation ID: {self.correlation_id}, Client ID: {self.client_id}"