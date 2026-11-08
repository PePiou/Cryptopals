import os

from set2.challenge9.padding import padd
from set2.challenge10.solution import ECB_decode, ECB_encode

BLOCK_SIZE = 16
AES_KEY = os.urandom(BLOCK_SIZE)


def parse(profile: str) -> dict[str, str]:
    result = {}
    for pair in profile.split("&"):
        key, value = pair.split("=")
        result[key] = value
    return result


def profile_for(email: str) -> str:
    email = email.replace("&", "").replace("=", "")
    return f"email={email}&uid=10&role=user"


def oracle(email: str) -> bytes:
    profile = profile_for(email).encode()
    return ECB_encode(padd(profile, BLOCK_SIZE), AES_KEY)


def solve() -> bytes:
    email_prefix = "A" * (BLOCK_SIZE - len("email="))
    padded_admin = padd(b"admin", BLOCK_SIZE).decode("ascii")
    ciphertext = oracle(email_prefix + padded_admin)
    admin_block = ciphertext[BLOCK_SIZE:2 * BLOCK_SIZE]

    profile_prefix_size = len("email=") + len("&uid=10&role=")
    email = "A" * (-profile_prefix_size % BLOCK_SIZE)
    user_profile = oracle(email)
    return user_profile[:-BLOCK_SIZE] + admin_block


def main() -> None:
    forged_profile = solve()
    print(forged_profile)
    print(ECB_decode(forged_profile, AES_KEY))


if __name__ == "__main__":
    main()
