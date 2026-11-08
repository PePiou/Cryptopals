import base64
from pathlib import Path

from Crypto.Cipher import AES


def solve() -> str:
    ciphertext = base64.b64decode(Path(__file__).with_name("7.txt").read_text(encoding="utf-8"))
    cipher = AES.new(b"YELLOW SUBMARINE", mode=AES.MODE_ECB)
    return cipher.decrypt(ciphertext).decode("utf-8")


def main():
    print(solve())


if __name__ == "__main__":
    main()
