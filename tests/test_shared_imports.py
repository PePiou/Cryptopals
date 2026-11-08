import hashlib
import importlib

import pytest
from Crypto.Cipher import AES
from Crypto.Util import Counter

from set2.challenge9.padding import padd
from set2.challenge10.solution import CBC_decode, CBC_encode
from set2.challenge15.solution import unpadd
from set3.challenge18.CTR_mode import CTR_decode, CTR_encode
from set3.challenge21.generateur import MTI19937
from set4.challenge28.sha1 import sha1


def test_cbc_padding_variants():
    key, iv = bytes(range(16)), bytes(reversed(range(16)))
    plaintext = b"Shared CBC across challenges"
    ciphertext = CBC_encode(plaintext, key, iv)
    assert ciphertext == AES.new(key, AES.MODE_CBC, iv).encrypt(padd(plaintext, 16))
    assert CBC_decode(ciphertext, key, iv) == plaintext
    assert CBC_decode(ciphertext, key, iv, validate_padding=True) == plaintext
    raw = bytes(range(32))
    ciphertext = CBC_encode(raw, key, iv, pad=False)
    assert CBC_decode(ciphertext, key, iv, unpad=False) == raw
    with pytest.raises(ValueError):
        CBC_decode(ciphertext, key, iv, validate_padding=True)


def test_padding_oracle_uses_strict_validation():
    from set3.challenge17.context import is_padding_valid

    key, iv = bytes(16), bytes(16)
    valid = CBC_encode(b"A" * 16, key, iv)
    invalid = CBC_encode(b"A" * 15 + b"\x00", key, iv, pad=False)
    assert is_padding_valid(valid, key, iv)
    assert not is_padding_valid(invalid, key, iv)


def test_challenge27_uses_raw_cbc():
    from set4.challenge27.context import encoding, key

    plaintext = b"A" * 32
    assert encoding(plaintext) == AES.new(key, AES.MODE_CBC, key).encrypt(plaintext)


@pytest.mark.parametrize("plaintext", [b"", b"A" * 15, b"A" * 16, b"A" * 17, b"A" * 30 + b"\x02\x02", bytes(range(64))])
def test_padding_oracle_recovers_message(plaintext):
    from set3.challenge17.context import is_padding_valid
    from set3.challenge17.solve import solve

    key, iv = bytes(range(16)), bytes(reversed(range(16)))
    ciphertext = CBC_encode(plaintext, key, iv)

    def padding_oracle(candidate):
        return is_padding_valid(candidate, key, iv)

    assert solve(ciphertext, iv, padding_oracle) == plaintext


@pytest.mark.parametrize("length", [0, 1, 15, 16, 17, 63])
def test_ctr_partial_blocks(length):
    key, nonce = bytes(range(16)), 42
    plaintext = bytes(range(length))
    counter = Counter.new(64, prefix=nonce.to_bytes(8, "little"), initial_value=0, little_endian=True)
    expected = AES.new(key, AES.MODE_CTR, counter=counter).encrypt(plaintext)
    assert CTR_encode(plaintext, key, nonce) == expected
    assert CTR_decode(expected, key, nonce) == plaintext


def test_shared_mt_reference_output():
    assert MTI19937(5489).random_number() == 3499211612
    for module in ("set3.challenge22.find_seed", "set3.challenge24.MTI19937_stream_cipher"):
        assert importlib.import_module(module).MTI19937 is MTI19937


def test_sha1_keeps_standard_hashing_and_resumable_state():
    from set4.challenge29.MAC import MAC
    from set4.challenge29.attack import attack

    key, message = b"secret key", b"message"
    assert sha1(message) == hashlib.sha1(message).hexdigest()
    forged_message, forged_mac = attack(message, MAC(message, key), len(key))
    assert forged_mac == MAC(forged_message, key)


def test_strict_unpadding():
    assert unpadd(padd(b"ICE ICE BABY", 16), 16) == b"ICE ICE BABY"
    with pytest.raises(ValueError):
        unpadd(b"ICE ICE BABY\x01\x02\x03\x04", 16)
