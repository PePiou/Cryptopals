import os

from set3.challenge18.CTR_mode import CTR_decode, CTR_encode

PREFIX = "comment1=cooking%20MCs;userdata="
SUFFIX = ";comment2=%20like%20a%20pound%20of%20bacon"
AES_KEY = os.urandom(16)
NONCE = 0


def encrypt_user_data(user_input: str) -> bytes:
    """Retire les s?parateurs de l'entr?e et chiffre le message en CTR."""
    user_input = user_input.replace(";", "").replace("=", "")
    plaintext = (PREFIX + user_input + SUFFIX).encode()
    return CTR_encode(plaintext, AES_KEY, NONCE)


def is_admin(ciphertext: bytes) -> bool:
    return b";admin=true;" in CTR_decode(ciphertext, AES_KEY, NONCE)
