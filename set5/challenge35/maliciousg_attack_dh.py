import secrets
import os

from set1.challenge3.solution3 import english_score
from set2.challenge10.solution import CBC_decode, CBC_encode
from set5.challenge33.diffle_hellman import modexp, secret_to_keys

class Participant:
    def __init__(self, nom: str):
        self.nom = nom
        self.p = None
        self.g = None
        self.prive = None
        self.public = None
        self.public_autre = None
        self.secret = None
        self.cle_aes = None
        self.message_received = None

    def preparer(self, p: int, g: int):
        self.p = p
        self.g = g

    def send_parametres(self, other):
        return other.recevoir_parametres(self.p, self.g)

    def recevoir_parametres(self, p: int, g: int):
        self.preparer(p, g)
        return "ACK"

    def generer_cles(self):
        self.prive = secrets.randbelow(self.p - 1) + 1
        self.public = modexp(self.g, self.prive, self.p)

    def send_public_key(self, other):
        other.public_autre = self.public

    def calculate_secret(self):
        self.secret = modexp(self.public_autre, self.prive, self.p)
        self.cle_aes = secret_to_keys(self.secret, self.p)[0]

    def send_cipher(self, cipher: bytes, other):
        other.message_received = other.dechiffrer(cipher)

    def chiffrer(self, msg: bytes):
        iv = os.urandom(16)
        return CBC_encode(msg, self.cle_aes, iv) + iv

    def dechiffrer(self, cipher: bytes):
        iv = cipher[-16:]
        return CBC_decode(cipher[:-16], self.cle_aes, iv)


class Attaquant:
    def __init__(self, nom: str):
        self.nom = nom
        self.p = None
        self.g = None
        self.cles_candidates = []
        self.cle_aes = None
        self.public_1 = None
        self.public_2 = None
        self.messages = []

    def intercepter_demande(self, p: int, g_malveillant: int):
        self.p = p
        self.g = g_malveillant

        return self.p, self.g

    def intercepter_public(self, public_1: int):
        self.public_1 = public_1
        return public_1

    def intercepter_reponse(self, public_2: int):
        self.public_2 = public_2
        return public_2

    def preparer_cle(self):
        match self.g:
            case 1:
                secrets_supposes = [1]
            case valeur if valeur == self.p:
                secrets_supposes = [0]
            case valeur if valeur == self.p - 1:
                secrets_supposes = [1, self.p - 1]
            case _:
                raise ValueError("Valeur de g non prévue")

        self.cles_candidates = [secret_to_keys(secret, self.p)[0] for secret in secrets_supposes]

    def intercept_cipher(self, cipher: bytes):
        iv = cipher[-16:]
        candidats = []

        for cle in self.cles_candidates:
            try:
                message = CBC_decode(cipher[:-16], cle, iv)
            except ValueError:
                continue

            candidats.append((message, cle))

        message, cle = max(candidats, key=lambda candidat: english_score(candidat[0]))

        self.cle_aes = cle
        self.messages.append(message)
        return cipher

def main():
    p_hex = "ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff"
    p = int(p_hex, 16)
    g = 2
    g_malveillant = p

    msg = b"i love you when i drink champagne i love you when i drink champagne i love you when i drink champagne i love you when i drink champagne i love you when i drink champagne i love you when i drink champagne"

    Alice = Participant("Alice")
    Bob = Participant("Bob")
    Mallory = Attaquant("Mallory")

    Alice.preparer(p, g_malveillant)

    p_recu, g_recu = Mallory.intercepter_demande(Alice.p, g_malveillant)
    ack = Bob.recevoir_parametres(p_recu, g_recu)

    if ack != "ACK":
        raise ValueError("Paramètres pas reçus")

    Alice.generer_cles()
    Bob.generer_cles()

    Bob.public_autre = Mallory.intercepter_public(Alice.public)
    Alice.public_autre = Mallory.intercepter_reponse(Bob.public)

    Alice.calculate_secret()
    Bob.calculate_secret()

    cipher = Alice.chiffrer(msg)

    Mallory.preparer_cle()
    cipher = Mallory.intercept_cipher(cipher)

    Alice.send_cipher(cipher, Bob)

    cipher_retour = Mallory.intercept_cipher(Bob.chiffrer(Bob.message_received))
    Bob.send_cipher(cipher_retour, Alice)

    print(Mallory.messages[-1:])
    print(Alice.message_received)
    print(Bob.message_received)

if __name__ == "__main__":
    main()
