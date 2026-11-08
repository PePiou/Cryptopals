import base64
import os
import random

from set2.challenge10.solution import CBC_decode, CBC_encode

BLOCK_SIZE = 16
MESSAGES_BASE64 = [
    "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
    "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
    "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
    "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
    "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
    "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
    "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
    "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
    "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
    "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
]

def generate_ciphertext() -> tuple[bytes, bytes, bytes]:
    """Choisit un message et renvoie son chiffré, la clé et l'IV."""
    plaintext = base64.b64decode(random.choice(MESSAGES_BASE64))
    key = os.urandom(BLOCK_SIZE)
    iv = os.urandom(BLOCK_SIZE)
    return CBC_encode(plaintext, key, iv), key, iv


def is_padding_valid(ciphertext: bytes, key: bytes, iv: bytes) -> bool:
    """Ne révèle que la validité du padding après déchiffrement."""
    try:
        CBC_decode(ciphertext, key, iv, validate_padding=True)
    except ValueError:
        return False
    return True
