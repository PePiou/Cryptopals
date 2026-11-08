import os

from set2.challenge10.solution import CBC_decode, CBC_encode

BLOCK_SIZE = 16
PREFIX = "comment1=cooking%20MCs;userdata="
SUFFIX = ";comment2=%20like%20a%20pound%20of%20bacon"
AES_KEY = os.urandom(BLOCK_SIZE)
IV = os.urandom(BLOCK_SIZE)


def encrypt_user_data(user_input: str) -> bytes:
    """Retire les séparateurs de l'entrée et chiffre le message en CBC."""
    user_input = user_input.replace(";", "").replace("=", "")
    plaintext = (PREFIX + user_input + SUFFIX).encode()
    return CBC_encode(plaintext, AES_KEY, IV)


def is_admin(ciphertext: bytes) -> bool:
    """Vérifie la présence du marqueur administrateur après déchiffrement."""
    return b";admin=true;" in CBC_decode(ciphertext, AES_KEY, IV)
