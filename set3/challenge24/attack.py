from set3.challenge24.MTI19937_stream_cipher import chosen_cipher, decrypt


def break_MTI19937() -> int | str:
    ciphertext = chosen_cipher()
    known_suffix = b"A" * 14
    for seed in range(2**16):
        if decrypt(ciphertext, seed).endswith(known_suffix):
            return seed
    return "seed not found"


if __name__ == "__main__":
    print(break_MTI19937())
