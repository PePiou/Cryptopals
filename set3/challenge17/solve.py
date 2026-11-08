from collections.abc import Callable

from set2.challenge10.solution import xor
from set2.challenge15.solution import unpadd
from set3.challenge17.context import BLOCK_SIZE, generate_ciphertext, is_padding_valid

PaddingOracle = Callable[[bytes], bool]


def recover_byte(
    previous_block: bytes,
    current_block: bytes,
    padding_size: int,
    padding_oracle: PaddingOracle,
) -> int:
    for difference in range(256):
        candidate = bytearray(previous_block)
        candidate[-padding_size] ^= difference
        if not padding_oracle(bytes(candidate) + current_block):
            continue
        if padding_size < BLOCK_SIZE:
            candidate[-(padding_size + 1)] ^= 1
            if not padding_oracle(bytes(candidate) + current_block):
                continue
        return difference ^ padding_size


def recover_block(
    previous_block: bytes, current_block: bytes, padding_oracle: PaddingOracle
) -> bytes:
    recovered = bytearray()
    for known_size in range(BLOCK_SIZE):
        padding_size = known_size + 1
        candidate = bytearray(previous_block)
        if known_size:
            candidate[-known_size:] = xor(
                xor(candidate[-known_size:], recovered),
                bytes([padding_size]) * known_size,
            )
        plaintext_byte = recover_byte(
            bytes(candidate), current_block, padding_size, padding_oracle
        )
        recovered.insert(0, plaintext_byte)
    return bytes(recovered)


def solve(ciphertext: bytes, iv: bytes, padding_oracle: PaddingOracle) -> bytes:
    blocks = [iv] + [
        ciphertext[start:start + BLOCK_SIZE]
        for start in range(0, len(ciphertext), BLOCK_SIZE)
    ]
    plaintext = b""
    for index in range(len(blocks) - 1, 0, -1):
        plaintext = recover_block(blocks[index - 1], blocks[index], padding_oracle) + plaintext
    return unpadd(plaintext, BLOCK_SIZE)


def main() -> None:
    ciphertext, key, iv = generate_ciphertext()
    def padding_oracle(candidate: bytes) -> bool:
        return is_padding_valid(candidate, key, iv)
    print(solve(ciphertext, iv, padding_oracle))


if __name__ == "__main__":
    main()
