import os
import random

from set3.challenge21.generateur import MTI19937

SEED = random.randrange(2**16)


def encrypt(plaintext: bytes, key: int = SEED) -> bytes:
    mask = b""
    generator = MTI19937(key)
    for _ in range(len(plaintext) // 4 + 1):
        mask += generator.random_number().to_bytes(4, "big")
    return bytes(a ^ b for a, b in zip(plaintext, mask))


def decrypt(ciphertext: bytes, key: int = SEED) -> bytes:
    return encrypt(ciphertext, key)


def chosen_cipher() -> bytes:
    prefix = os.urandom(random.randint(50, 100))
    known_suffix = b"A" * 14
    return encrypt(prefix + known_suffix, SEED)
