from set2.challenge10.solution import ECB_encode, xor


def edit(
    ciphertext: bytes, key: bytes, offset: int, newtext: bytes, nonce: int = 0
) -> bytes:
    """Remplace une portion du texte en recalculant son chiffr? CTR."""
    block_size = 16
    end = offset + len(newtext)
    first_block = offset // block_size
    last_block = end // block_size
    keystream = b""
    for block_index in range(first_block, last_block + 1):
        counter = nonce.to_bytes(8, "little") + block_index.to_bytes(8, "little")
        keystream += ECB_encode(counter, key)

    stream_start = offset % block_size
    replacement = xor(keystream[stream_start:stream_start + len(newtext)], newtext)
    return ciphertext[:offset] + replacement + ciphertext[end:]
