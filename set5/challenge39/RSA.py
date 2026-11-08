from set5.challenge33.diffle_hellman import modexp

def euclide(a: int, b: int) -> tuple[int, int, int]:
    u, v = 1, 0
    x, y = 0, 1

    while b != 0:
        q = a // b

        a, b = b, a - q * b
        u, x = x, u - q * x
        v, y = y, v - q * y

    return a, u, v

def euler(p: int, q: int) -> int:
    return (p-1) * (q-1)

def gen_private_key(public_key: tuple[int, int], et: int) -> tuple[int, int]:
    a, u, _= euclide(public_key[0], et)
    if a != 1:
        raise ValueError("no modular inverse")
    return u % et, public_key[1]

def rsa_encrypt(public_key: tuple[int, int], plaintext: int) -> int:
    return modexp(plaintext, public_key[0], public_key[1])

def rsa_decrypt(private_key: tuple[int, int], ciphertext: int) -> int:
    return modexp(ciphertext, private_key[0], private_key[1])

def str_to_int(input: str) -> int:
    return int.from_bytes(input.encode("utf-8"), byteorder="big")

def int_to_str(input: int) -> str:
    length = (input.bit_length() + 7) //8
    return input.to_bytes(length, byteorder="big").decode("utf-8")

def main():
    plain = "i wan't to break free ! I wan't to breaaak freee !"
    p = 2**521 - 1
    q = 2**607 - 1
    e = 65537
    n = p * q
    et = euler(p, q)
    d = gen_private_key((e, n), et)[0]
    m = str_to_int(plain)
    cipher = rsa_encrypt((e, n), m)
    print(cipher)
    plainagain= rsa_decrypt((d, n), cipher)
    plainagain = int_to_str(plainagain)
    print(plainagain)

if __name__ == "__main__":
    main()
