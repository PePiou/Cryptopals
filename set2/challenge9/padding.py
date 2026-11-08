def padd(byte_input: bytes, block_length: int) -> bytes:
    n = block_length - len(byte_input) % block_length
    return byte_input + bytes([n] * n)

if __name__ == "__main__":
    s = b"YELLOW SUBMARINE"
    print(padd(s, 20))
