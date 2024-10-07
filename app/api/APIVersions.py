from .ErrorCode import ErrorCode

class _KafkaRequest:
    SUPPORTED_API_VERSIONS = [0, 1, 2, 3, 4]

    def __init__(self, data: bytes, size: int=1024):
        if len(data) > size:
            raise ValueError("Invalid header size")
        self.data = data
        # Extract the API key from the datauest
        self.api_key = int.from_bytes(data[4:6], byteorder='big') 

        # Extract the API version from the dataues
        self.api_version = int.from_bytes(data[6:8], byteorder='big')

        # Extract the correlation ID from the datauest
        self.correlation_id = int.from_bytes(data[8:12], byteorder='big')

        # Extract the client ID from the datauest
        self.client_id = None

        self.size = size
    
    def isAllowed(self) -> bool:
        return self.api_version in self.SUPPORTED_API_VERSIONS
    
    def __str__(self):
        return f"-> Kafka Request: API Key: {self.api_key}, API Version: {self.api_version}, Correlation ID: {self.correlation_id}, Client ID: {self.client_id}"
    
class _Body:
    def __init__(self, error: int = 0):
        self.error = error
        self.api_key = 18
        self.min_version = 0
        self.max_version = 4
        self.tag_buffer = b"\x00"
        self.throttle_time_ms = 0

        self.data = (
            self.error.to_bytes(2, byteorder='big', signed=True) +
            int(2).to_bytes(1, byteorder='big', signed=True) +
            self.api_key.to_bytes(2, byteorder='big', signed=True) +
            self.min_version.to_bytes(2, byteorder='big', signed=True) +
            self.max_version.to_bytes(2, byteorder='big', signed=True) +
            self.tag_buffer +
            self.throttle_time_ms.to_bytes(4, byteorder='big', signed=True) +
            self.tag_buffer
        )

    def __str__(self):
        return f"Error: {self.error}, API Key: {self.api_key}, Min Version: {self.min_version}, Max Version: {self.max_version}, Tag Buffer: {self.tag_buffer}, Throttle Time: {self.throttle_time_ms}"  


class APIVersions:
    def __init__(self, data: bytes):
        self.kafka_request = _KafkaRequest(data)
        print(self.kafka_request)
        self.body = _Body(
            error = ErrorCode.NO_ERROR.value 
            if self.kafka_request.isAllowed() else ErrorCode.UNSUPPORTED_VERSION.value
        )
        print(self.body)
        
        self.response_header = self.kafka_request.correlation_id.to_bytes(4, byteorder='big', signed=True)
        self.size = len(self.response_header + self.body.data)

    
    def to_bytes(self):
        return self.size.to_bytes(4, byteorder='big', signed=True) + self.response_header + self.body.data