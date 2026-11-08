from set1.challenge3.solution3 import decrypt_sbxor
from set1.challenge6.find_keysize import lecture


def decouper(bytes_input: bytes, keysize: int) -> list[bytes]:
    return [bytes_input[i:i + keysize] for i in range(0, len(bytes_input), keysize)]


def reorganize(decoupage: list[bytes]) -> list[bytes]:
    return [
        bytes(block[i] for block in decoupage if i < len(block))
        for i in range(max(map(len, decoupage), default=0))
    ]


def find_plaintext(list_input: list[bytes]) -> list[bytes]:
    return [decrypt_sbxor(block)["plaintext"] for block in list_input]


def main() -> None:
    blocks = decouper(lecture(), 29)
    columns = reorganize(blocks)
    plaintext = b"".join(reorganize(find_plaintext(columns)))
    print(plaintext.decode("utf-8"))


if __name__ == "__main__":
    main()
