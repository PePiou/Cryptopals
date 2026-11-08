from pathlib import Path

import base64

from set1.challenge6.hamming_distance import average_distance


def lecture() -> bytes:
    with open(Path(__file__).with_name("ciphertext_challenge6.txt"), encoding="utf-8") as f:
        return base64.b64decode(f.read())


def main() -> None:
    code = lecture()
    candidates = [
        {"keysize": keysize, "score": average_distance(code, keysize)}
        for keysize in range(2, 40)
    ]
    print(min(candidates, key=lambda candidate: candidate["score"]))


if __name__ == "__main__":
    main()
