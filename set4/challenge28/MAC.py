from set4.challenge28.sha1 import sha1


def MAC(message: bytes, key: bytes) -> str:
    """Calcule le MAC avec la cl? plac?e apr?s le message."""
    return sha1(message + key)
