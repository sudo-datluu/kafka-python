from typing import Callable, Any, Optional

class Encoder:
    EncodeFunction = Callable[[Any], bytes]
    @staticmethod
    def encode_int8(integer: int) -> bytes:
        return integer.to_bytes(1, signed=True)

    @staticmethod
    def encode_int16(integer: int) -> bytes:
        return integer.to_bytes(2, signed=True)

    @staticmethod
    def encode_int32(integer: int) -> bytes:
        return integer.to_bytes(4, signed=True)

    @staticmethod
    def encode_int64(integer: int) -> bytes:
        return integer.to_bytes(8, signed=True)

    @staticmethod
    def encode_tagged_fields() -> bytes:
        return b"\x00"
    
    @staticmethod
    def encode_varint(interger: int) -> bytes:
        # Convert the interger to a signed 32-bit interger
        if interger < 0:
            interger += 1 << 32
        BASE = 128
        encoding = b""

        # Loop until the interger is 0
        while True:
            interger, byte = divmod(interger, BASE)
            if interger > 0:
                byte += BASE
            encoding += byte.to_bytes(1, byteorder="big")
            if interger == 0: return encoding


    @staticmethod
    def encode_compact_array(array: list, encode_function: Optional[EncodeFunction] = None) -> bytes:
        encoding_items = b"".join(
            item.encode() if encode_function is None else encode_function(item)
            for item in array
        )
        return Encoder.encode_varint(len(array) + 1) + encoding_items
