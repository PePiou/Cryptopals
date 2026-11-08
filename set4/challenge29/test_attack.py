from set4.challenge29.MAC import MAC
from set4.challenge29.attack import attack, md_padding


def test_attack() -> None:
    key = b"1234567812345678"
    message = (
        b"Put your head on my shoulder Hold me in your arms, baby "
        b"Squeeze me oh-so-tight Show me that you love me too "
        b"Put your lips next to mine, dear Won't you kiss me once, baby? "
        b"Just a kiss goodnight, maybe You and I will fall in love "
        b"(you and I will fall in love"
    )
    glue_padding = md_padding(b"\x00" * len(key) + message)
    expected_message = message + glue_padding + b";admin=true"
    signature = MAC(message, key)
    forged_message, forged_signature = attack(message, signature, len(key))

    assert forged_message == expected_message
    assert forged_signature == MAC(expected_message, key)
