from set4.challenge27.context import encoding
from set4.challenge27.context import decoding

USER_INPUT = b"YABAYABAYOBOYOBOYUBUYUBUYIBIYIBI"

cipher = encoding(USER_INPUT)
cipher_modified = cipher[:16] + b"\x00" * 16 + cipher[:16]

plain_modified = decoding(cipher_modified)
if plain_modified != b"":
    key = bytes(a ^ b for a, b in zip(plain_modified[:16], plain_modified[32:]))
print(key)
