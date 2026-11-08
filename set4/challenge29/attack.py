import struct

from set4.challenge28.sha1 import sha1


def md_padding(message: bytes) -> bytes:
    original_length = len(message)
    padding = b"\x80"
    while (original_length + len(padding)) % 64 != 56:
        padding += b"\x00"
    return padding + struct.pack(">Q", original_length * 8)


def find_state(signature: bytes) -> tuple[int, ...]:
    return tuple(
        int.from_bytes(signature[start:start + 4], "big")
        for start in range(0, 20, 4)
    )


def attack(message: bytes, signature: str, key_length: int) -> tuple[bytes, str]:
    """Prolonge le message sign? en reprenant SHA-1 depuis son ?tat final."""
    state = find_state(bytes.fromhex(signature))
    glue_padding = md_padding(b"\x00" * key_length + message)
    suffix = b";admin=true"
    processed_length = key_length + len(message) + len(glue_padding)
    forged_signature = sha1(suffix, state=state, processed_length=processed_length)
    return message + glue_padding + suffix, forged_signature
