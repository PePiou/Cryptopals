from set4.challenge30.MD4 import md4

def MAC(key: bytes, message: bytes) -> bytes:
    return md4(key + message)
