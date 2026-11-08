from set2.challenge10.solution import xor
from set4.challenge26.context import PREFIX, encrypt_user_data, is_admin


def solve() -> bool:
    """Injecte le marqueur admin en modifiant directement le chiffr? CTR."""
    known_plaintext = b"0" * 16
    target = b";admin=true;" + b"0" * 4
    ciphertext = encrypt_user_data(known_plaintext.decode("ascii"))
    start = len(PREFIX.encode())
    end = start + len(known_plaintext)
    modified = xor(xor(ciphertext[start:end], known_plaintext), target)
    forged_ciphertext = ciphertext[:start] + modified + ciphertext[end:]
    return is_admin(forged_ciphertext)


if __name__ == "__main__":
    print(solve())
