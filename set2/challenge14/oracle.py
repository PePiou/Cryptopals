import base64
import os
import random

from set2.challenge9.padding import padd
from set2.challenge10.solution import ECB_encode

BLOCK_SIZE = 16
KEY = os.urandom(BLOCK_SIZE)
RANDOM_PREFIX = os.urandom(random.randint(0, 256))
SECRET = base64.b64decode(
    "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
    "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
    "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
    "YnkK"
)


def oracle(user_input: bytes) -> bytes:
    """Chiffre le préfixe fixe, l'entrée et le secret en AES-ECB."""
    plaintext = RANDOM_PREFIX + user_input + SECRET
    return ECB_encode(padd(plaintext, BLOCK_SIZE), KEY)
