def hex_xor(hex1: str, hex2: str) -> str:
    a = bytes.fromhex(hex1)
    b = bytes.fromhex(hex2)
    return bytes(a ^ b for a, b in zip(a, b)).hex()

def main():
    hex1 = "1c0111001f010100061a024b53535009181c"
    hex2 = "686974207468652062756c6c277320657965"
    print(hex_xor(hex1, hex2) == "746865206b696420646f6e277420706c6179")

if __name__ == "__main__":
    main()
