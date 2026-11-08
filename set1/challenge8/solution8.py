from pathlib import Path

def hex_to_bytes(ciphertext: str) -> bytes:
    return(bytes.fromhex(ciphertext))

def detect_ECB(ciphertext: bytes) -> bool:
    blocks = [ciphertext[i : i + 16] for i in range(0, len(ciphertext), 16)]
    return len(set(blocks)) != len(blocks)

def find_ECB() -> bytes:
    with open(Path(__file__).with_name("8.txt"), "r", encoding="utf-8") as f:
        for line in f:
            line = hex_to_bytes(line.strip())
            if detect_ECB(line) == True:
                return line
        return "Rien trouvé"

print(find_ECB().hex())
