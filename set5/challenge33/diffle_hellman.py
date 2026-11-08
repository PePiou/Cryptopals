import hashlib
import secrets

p_hex = (
    "ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74"
    "020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f1437"
    "4fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7ed"
    "ee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf05"
    "98da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb"
    "9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff"
)

p = int(p_hex, 16)
g = 2

def modexp(base: int, exponent: int, modulus: int) -> int:
    bits = format(exponent, "b")
    result = 1
    factor = base
    for i in range(len(bits) - 1, -1, -1):
        if bits[i] == "1":
            result *= factor
            result %= modulus
        factor **= 2
        factor %= modulus
    return result

def generate_key(modulus: int, base: int) -> tuple[int, int]:
    exponent = secrets.randbelow(modulus)
    return exponent, modexp(base, exponent, modulus)


def create_secret(private_key: int, other_public_key: int, modulus: int) -> int:
    return modexp(other_public_key, private_key, modulus)


def secret_to_keys(secret: int, modulus: int) -> tuple[bytes, bytes]:
    size = -(-modulus.bit_length() // 8)
    secret_bytes = secret.to_bytes(size, "big")
    key_material = hashlib.sha256(secret_bytes).digest()
    encryption_key = key_material[:16]
    mac_key = key_material[16:]
    return encryption_key, mac_key

def main() -> None:
    a, A = generate_key(p, g)
    b, B = generate_key(p, g)
    secret_a = create_secret(a, B, p)
    secret_b = create_secret(b, A, p)
    key_a = secret_to_keys(secret_a, p)
    key_b = secret_to_keys(secret_b, p)
    assert key_a == key_b


if __name__ == "__main__":
    main()
