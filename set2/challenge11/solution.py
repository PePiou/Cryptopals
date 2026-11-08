from set2.challenge9.padding import padd
from set2.challenge10.solution import CBC_encode, ECB_encode, separate, xor

import os
import random








def generate_AES_key() -> bytes:
    return os.urandom(16)

def random_key_encrypt(plaintext: bytes) -> bytes:
    key = generate_AES_key()
    bit = random.randint(0,1)
    i, j = random.randint(5, 10), random.randint(5, 10)
    b1, b2 = os.urandom(i), os.urandom(j)

    if bit == 0:
        return ECB_encode(padd(b1 + plaintext + b2, 16), key)
    else:
        return CBC_encode(b1 + plaintext + b2, key, IV=os.urandom(16))

def find_encoding() -> str:
    ciphertext = random_key_encrypt(b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    blocks = [ciphertext[i : i + 16] for i in range(0, len(ciphertext), 16)]
    if len(set(blocks)) != len(blocks):
        return "ECB"
    else:
        return "CBC"


print(find_encoding())
