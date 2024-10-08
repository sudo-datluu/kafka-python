import io
import uuid
import typing

class Decoder:
    DecoderFunc = typing.Callable[[io.BytesIO], typing.Any]

    @staticmethod
    def decode_int8(byte_stream: io.BytesIO) -> int:
        return int.from_bytes(byte_stream.read(1), signed=True)

    @staticmethod
    def decode_int16(byte_stream: io.BytesIO) -> int:
        return int.from_bytes(byte_stream.read(2), signed=True)

    @staticmethod
    def decode_int32(byte_stream: io.BytesIO) -> int:
        return int.from_bytes(byte_stream.read(4), signed=True)

    @staticmethod
    def decode_int64(byte_stream: io.BytesIO) -> int:
        return int.from_bytes(byte_stream.read(8), signed=True)

    @staticmethod
    def decode_compact_array(byte_stream: io.BytesIO, decoder: DecoderFunc) -> list:
        num_entries = Decoder.decode_int32(byte_stream)
        return [decoder(byte_stream) for _ in range(num_entries)]

    @staticmethod
    def decode_nullable_string(byte_stream: io.BytesIO) -> str:
        length = Decoder.decode_int16(byte_stream)
        return "" if length < 0 else byte_stream.read(length).decode('utf-8')
    

    # Implment tagged fields in the future
    # TAG_BUFFER is always 0x00 - Null byte
    @staticmethod
    def decode_tagged_fields(byte_stream: io.BufferedIOBase) -> None:
        assert byte_stream.read(1) == b'\x00', "Tagged fields not supported"