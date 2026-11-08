import os
import secrets

from set2.challenge10.solution import CBC_decode, CBC_encode
from set5.challenge33.diffle_hellman import g, modexp, p, secret_to_keys


class Participant:
    def __init__(self, nom: str) -> None:
        self.nom = nom
        self.p = None
        self.g = None
        self.prive = None
        self.public = None
        self.public_autre = None
        self.secret = None
        self.cle_aes = None
        self.message_received = None

    def preparer(self, p: int, g: int) -> None:
        self.p = p
        self.g = g
        self.prive = secrets.randbelow(p - 1) + 1
        self.public = modexp(g, self.prive, p)

    def send_public_key(self, other: "Participant") -> None:
        other.public_autre = self.public

    def calculate_secret(self) -> None:
        self.secret = modexp(self.public_autre, self.prive, self.p)

    def send_cipher(self, cipher: bytes, other: "Participant") -> None:
        other.message_received = other.dechiffrer(cipher)

    def chiffrer(self, message: bytes) -> bytes:
        self.cle_aes = secret_to_keys(self.secret, self.p)[0]
        iv = os.urandom(16)
        return CBC_encode(message, self.cle_aes, iv) + iv

    def dechiffrer(self, cipher: bytes) -> bytes:
        iv = cipher[-16:]
        key = secret_to_keys(self.secret, self.p)[0]
        return CBC_decode(cipher[:-16], key, iv)


class Attaquant:
    def __init__(self, nom: str) -> None:
        self.nom = nom
        self.p = None
        self.g = None
        self.cle_aes = None
        self.public_1 = None
        self.public_2 = None
        self.messages = []

    def intercepter_demande(self, p: int, g: int, public_1: int) -> tuple[int, int, int]:
        self.public_1 = public_1
        self.p = p
        self.g = g

        # Remplacer la cl? publique par p force le secret partag? ? z?ro.
        return p, g, p

    def intercepter_reponse(self, public_2: int) -> int:
        self.public_2 = public_2

        return self.p

    def preparer_cle(self) -> None:
        self.cle_aes = secret_to_keys(0, self.p)[0]

    def intercept_cipher(self, cipher: bytes) -> bytes:
        iv = cipher[-16:]
        self.messages.append(CBC_decode(cipher[:-16], self.cle_aes, iv))
        return cipher


def main() -> None:
    message = b"The sea forgets the names we write, Yet keeps our footsteps through the night." * 6
    message = message.rstrip()

    alice = Participant("Alice")
    bob = Participant("Bob")
    mallory = Attaquant("Mallory")

    alice.preparer(p, g)
    bob.p, bob.g, bob.public_autre = mallory.intercepter_demande(
        p, g, alice.public
    )
    bob.preparer(bob.p, bob.g)
    alice.public_autre = mallory.intercepter_reponse(bob.public)

    alice.calculate_secret()
    bob.calculate_secret()

    mallory.preparer_cle()

    bob.message_received = bob.dechiffrer(
        mallory.intercept_cipher(alice.chiffrer(message))
    )

    alice.message_received = alice.dechiffrer(
        mallory.intercept_cipher(bob.chiffrer(bob.message_received))
    )

    print(alice.message_received)
    print(bob.message_received)
    print(mallory.messages[0])


if __name__ == "__main__":
    main()
