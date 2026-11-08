from set2.challenge10.solution import ECB_encode

CIPHER = b"L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
KEY = b"YELLOW SUBMARINE"
NONCE = 0

def CTR_encode(plaintext: bytes, key=KEY, nonce=NONCE) -> bytes:
    cipher = b""
    for count in range(len(plaintext) // 16):
        cipher += bytes(a ^ b for a, b in zip(plaintext[16 * count : 16 * (count + 1)], ECB_encode(nonce.to_bytes(8, "little") + count.to_bytes(8,"little"), key)))
    count = len(plaintext) // 16
    cipher += bytes(a ^ b for a, b in zip(plaintext[len(plaintext) // 16 * 16 :], ECB_encode(nonce.to_bytes(8, "little") + count.to_bytes(8, "little"), key)))
    return cipher

def CTR_decode(ciphertext: bytes, key=KEY, nonce=NONCE):
    plain = b""
    for count in range(len(ciphertext) // 16):
        bloc = ECB_encode(nonce.to_bytes(8, "little") + count.to_bytes(8,"little"), key)
        plain += bytes(a ^ b for a, b in zip(bloc, ciphertext[16 * count : 16 * (count + 1)]))
    count = len(ciphertext) // 16
    last_bloc = ECB_encode(nonce.to_bytes(8, "little") + count.to_bytes(8,"little"), key)
    plain += bytes(a ^ b for a, b in zip(last_bloc, ciphertext[len(ciphertext) // 16 * 16 :]))
    return plain


if __name__ == "__main__":
    print(CTR_encode(b"hello world hello world"))
