def unpadd(plaintext: bytes, block_size: int) -> bytes:
    if not 1 <= block_size <= 255:
        raise ValueError("padding incorrect")
    if not plaintext or len(plaintext) % block_size != 0:
        raise ValueError("padding incorrect")
    k = plaintext[-1]
    if not 1 <= k <= block_size:
        raise ValueError("padding incorrect")
    expected_padding = bytes([k]) * k
    if plaintext[-k:] != expected_padding:
        raise ValueError("padding incorrect")
    return plaintext[:-k]
