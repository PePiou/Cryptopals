from set2.challenge10.solution import CBC_encode
from set2.challenge10.solution import CBC_decode

import os

key = os.urandom(16)
USER_INPUT = b"YABAYABAYOBOYOBOYUBUYUBUYIBIYIBI"

def ASCII_compliance(data: bytes) -> bool:
    return all(byte < 128 for byte in data)

def encoding(user_input: bytes) -> bytes:
    return CBC_encode(user_input, key, key, pad=False)

def decoding(ciphertext: bytes) -> bytes:
    plaintext = CBC_decode(ciphertext, key, key, unpad=False)
    print("Résultat du déchiffrement :", repr(plaintext), len(plaintext))
    if not ASCII_compliance(plaintext):
        return plaintext
    else:
        return b""
