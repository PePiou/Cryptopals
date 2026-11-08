import os

from set1.challenge7.solution7 import solve as decrypt_challenge7
from set2.challenge10.solution import xor
from set3.challenge18.CTR_mode import CTR_encode
from set4.challenge25.edit_oracle import edit


def recover_plaintext(ciphertext: bytes, key: bytes) -> bytes:
    """Retrouve le message gr?ce au remplacement par un texte connu."""
    known_plaintext = b"0" * len(ciphertext)
    edited_ciphertext = edit(ciphertext, key, 0, known_plaintext)
    return xor(xor(ciphertext, edited_ciphertext), known_plaintext)


def main() -> None:
    key = os.urandom(16)
    plaintext = decrypt_challenge7().encode("utf-8")
    ciphertext = CTR_encode(plaintext, key)
    print(recover_plaintext(ciphertext, key))


if __name__ == "__main__":
    main()
