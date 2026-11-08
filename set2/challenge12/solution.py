import base64
import os

from set2.challenge9.padding import padd
from set2.challenge10.solution import ECB_encode

BLOCK_SIZE = 16
KEY = os.urandom(16)
SECRET = base64.b64decode(
    "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg"
    "aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq"
    "dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg"
    "YnkK"
)


def oracle(user_input: bytes) -> bytes:
    plaintext = user_input + SECRET
    return ECB_encode(padd(plaintext, BLOCK_SIZE), KEY)


def find_block_size() -> int:
    ciphertext = oracle(b"A" * 100)
    for block_size in range(2, 40):
        if ciphertext[:block_size] == ciphertext[block_size:2 * block_size]:
            return block_size


def solve() -> bytes:
    block_size = find_block_size()
    prefix_size = block_size - 1
    recovered = b"A" * prefix_size

    for position in range(len(SECRET)):
        block_start = (position // block_size) * block_size
        padding = b"A" * (prefix_size - position % block_size)
        target = oracle(padding)[block_start:block_start + block_size]

        known = recovered[-prefix_size:]
        for candidate in range(256):
            test = known + bytes([candidate])
            if oracle(test)[:block_size] == target:
                recovered += bytes([candidate])
                break
    return recovered[prefix_size:]


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
