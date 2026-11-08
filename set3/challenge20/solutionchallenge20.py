from pathlib import Path

import base64

from set3.challenge18.CTR_mode import CTR_encode
from set1.challenge3.solution3 import decrypt_sbxor

def decouper(bytes_input: bytes, KEYSIZE: int) -> list[str]:
    result = []
    for i in range(len(bytes_input)//KEYSIZE):
        result.append(bytes_input[i * KEYSIZE : (i + 1) * KEYSIZE])
    return(result)

def reorganize(decoupage: list[bytes]) -> list[bytes]:
    result = [[] for i in range(29)]
    for b in decoupage:
        for i in range(29):
            result[i].append(b[i])
    return [bytes(a) for a in result]

def find_plaintext(list_input: list[bytes]) -> str:
    key = ["" for i in range(29)]
    for i in range(29):
        key[i] = decrypt_sbxor(list_input[i]).get('plaintext')
    return key

def lecture() -> str:
    with open(Path(__file__).with_name("20.txt"), "r", encoding = "utf-8") as f:
        result = []
        for line in f:
            result.append(base64.b64decode(line.strip()))
            min_len = -1
        for e in result:
            if len(e) < min_len or min_len < 0:
                min_len = len(e)
        for i in range(len(result)):
            result[i] = result[i][:min_len]
        s = b""
        for e in result:
            s += CTR_encode(e)
        return s, min_len

plaintext, min_len = lecture()
print(plaintext)

def main():
    decoupage = decouper(plaintext, min_len)
    l = reorganize(decoupage)
    print(reorganize(find_plaintext(l)))

if __name__ == "__main__":
    main()
