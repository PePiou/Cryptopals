from pathlib import Path

from set1.challenge3.solution3 import decrypt_sbxor

def solution4():
    with open(Path(__file__).with_name("ciphertext_challenge4.txt"), "r", encoding="utf-8") as f:
        candidates=[]
        for line in f:
            l = line.strip()
            candidates.append(decrypt_sbxor(bytes.fromhex(l)))
    return sorted(candidates, key = lambda c: c['score'])[-1]

print(solution4())
