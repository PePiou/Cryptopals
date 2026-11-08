def xor(bytes_input: bytes, key: bytes) -> bytes:
    return bytes(a ^ key[i % len(key)] for i, a in enumerate(bytes_input)).hex()

def main():
    plaintext = b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    key = b"ICE"
    expected_hex = (
        "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
        )
    print(xor(plaintext,key) == expected_hex)

if __name__ == "__main__":
    main()
