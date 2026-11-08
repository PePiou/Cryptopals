import secrets
import hashlib
import hmac

from set5.challenge33.diffle_hellman import modexp, generate_key

def server_knowledge(pwd: str, N: int, g: int):
    salt = secrets.randbelow(N)
    x = generate_x(pwd, salt)
    v = modexp(g, x, N)
    return salt, v

def generate_client_key(N: int, g: int) -> tuple[int, int]:
    return generate_key(N, g)

def generate_server_key(N: int, g: int, k: int, v: int) -> tuple[int, int]:
    b, gb = generate_key(N, g)
    B = (k * v + gb) % N
    return b, B

def generate_u(A: int, B: int) -> int:
    data = (str(A) + str(B)).encode("utf-8")
    return int.from_bytes(hashlib.sha256(data).digest(), byteorder="big")

def generate_x(pwd: str, salt: int) -> int:
    data = (str(salt) + pwd).encode("utf-8")
    return int.from_bytes(hashlib.sha256(data).digest(), byteorder="big")

def generate_client_secret(B:int ,k:int ,g:int ,x:int ,a:int ,u: int, N:int) -> int:
    data = str(modexp(B - k * modexp(g, x, N), a + u * x, N)).encode("utf-8")
    return int.from_bytes(hashlib.sha256(data).digest(), byteorder="big")

def generate_server_secret(A:int ,v:int ,b:int ,N:int ,u: int) -> int:
    data = str(modexp(A * modexp(v, u, N), b, N)).encode("utf-8")
    return int.from_bytes(hashlib.sha256(data).digest(), byteorder="big")

def main():
    g = 2
    k = 3
    I = "email@gmail.com"
    P = "password"
    N_hex = "ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff"
    N = int(N_hex, 16)

    salt, v = server_knowledge(P, N, g)
    a, A = generate_key(N, g)
    b, B = generate_server_key(N, g, k, v)
    u = generate_u(A, B)
    x = generate_x(P, salt)
    s_client = generate_client_secret(B, k, g, x, a, u, N)
    s_server = generate_server_secret(A, v, b, N, u)

    client_mac = hmac.digest(
        s_client.to_bytes(32, "big"),
        str(salt).encode(),
        "sha256"
    )

    server_mac = hmac.digest(
        s_server.to_bytes(32, "big"),
        str(salt).encode(),
        "sha256"
    )

    assert hmac.compare_digest(client_mac, server_mac)

if __name__ == "__main__":
    main()
