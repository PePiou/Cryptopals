from set4.challenge28.sha1 import sha1


def MAC(message: bytes, key: bytes) -> str:
    """Secret-prefix MAC used by the length-extension challenge."""
    return sha1(key + message)
