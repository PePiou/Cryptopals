from pathlib import Path

from set2.challenge9.padding import padd
from set2.challenge15.solution import unpadd as validate_unpadd

from Crypto.Cipher import AES
import base64

KEY = b"YELLOW SUBMARINE"
IV = bytes(16)


def unpadd(byte_input: bytes) -> bytes:
    b = byte_input[-1]
    return byte_input[0 : len(byte_input) - b]

def separate(text: bytes, blocklength: int) -> list[bytes]:
    result = []
    for i in range(0, len(text), blocklength):
        result.append(text[i : i + blocklength])
    return result

def xor(b1: bytes, b2: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(b1,b2))



def ECB_decode(ciphertext: bytes, key: bytes, ) -> bytes:
    cipher = AES.new(key, mode=AES.MODE_ECB)
    return(cipher.decrypt(ciphertext))

def ECB_encode(plaintext: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, mode=AES.MODE_ECB)
    return(cipher.encrypt(plaintext))



def CBC_encode(plaintext: bytes, key: bytes, IV=bytes(16), *, pad=True) -> bytes:
    blocks = separate(padd(plaintext, 16) if pad else plaintext, 16)
    blocks[0] = ECB_encode(xor(blocks[0], IV), key)
    for i in range(1, len(blocks)):
        blocks[i] = ECB_encode(xor(blocks[i],blocks[i-1]), key)
    return b"".join(blocks)

def CBC_decode(cipher: bytes, key: bytes, IV=bytes(16), *, unpad=True, validate_padding=False) -> bytes:
    blocks = separate(cipher, 16)
    for i in range(len(blocks)-1, 0, -1):
        blocks[i] = xor(blocks[i-1], ECB_decode(blocks[i], key))
    blocks[0] = xor(ECB_decode(blocks[0], key), IV)
    plaintext = b"".join(blocks)
    if not unpad:
        return plaintext
    if validate_padding:
        return validate_unpadd(plaintext, 16)
    return unpadd(plaintext)

if __name__ == "__main__":
    with open(Path(__file__).with_name("10.txt"), "r", encoding = "utf-8") as f:
        ciphertext = base64.b64decode(f.read())
    plain = CBC_decode(ciphertext, KEY, IV)
    ciphertext = CBC_encode(plain, KEY, IV)
    a = CBC_decode(ciphertext, KEY, IV)
    print(a)
