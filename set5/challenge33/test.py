import hashlib
import random


def test_key_exchange() -> None:
    p = 37
    g = 5
    a = random.randrange(p)
    b = random.randrange(p)
    A = (g**a) % p
    B = (g**b) % p

    secret_a = (B**a) % p
    secret_b = (A**b) % p
    assert secret_a == secret_b

    size = (p.bit_length() + 7) // 8
    secret_bytes = secret_a.to_bytes(size, "big")
    key_material = hashlib.sha256(secret_bytes).digest()
    encryption_key = key_material[:16]
    mac_key = key_material[16:]
    assert len(encryption_key) == len(mac_key) == 16


if __name__ == "__main__":
    test_key_exchange()
    print(True)
