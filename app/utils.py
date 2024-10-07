def create_message(param_id: int, error: int | None = None) -> bytes:
    # Convert the integer to a 4-byte big-endian byte array
    msg = param_id.to_bytes(4, byteorder='big', signed=True)
    if error != None:
        msg += error.to_bytes(2, byteorder='big', signed=True)
    header = len(msg).to_bytes(4, byteorder='big', signed=True)
    return  header + msg