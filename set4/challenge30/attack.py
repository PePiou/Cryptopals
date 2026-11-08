from set4.challenge30.context import MAC
from set4.challenge30.MD4 import md4

import struct

def md_padding(message: bytes) -> bytes:
    original_length = len(message)

    padding = b'\x80'

    while (original_length + len(padding)) % 64 != 56:
        padding += b'\x00'

    padding += struct.pack('<Q', original_length * 8)

    return padding

key = b"1234567891234567"
key_length = len(key)
message = b"i love you when i drink champagne, i love you when i drink champagne, i love you when i drink champagne"
hash = MAC(key, message)
glue_padding = md_padding(b'\x00' * key_length + message)
new_message = message + glue_padding + b";admin=true"

def find_state(signature: bytes) -> list[int]:
    return list(struct.unpack("<4I", signature))

print(md4(b";admin=true", state=find_state(hash), length_processed=len(key) + len(message) + len(glue_padding)))
print(MAC(key, new_message))
