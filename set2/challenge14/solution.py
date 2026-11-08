from set2.challenge14.oracle import BLOCK_SIZE, oracle


def find_alignment() -> tuple[int, int]:
    """Trouve le début des blocs contrôlés et le padding qui les aligne."""
    for padding_length in range(BLOCK_SIZE):
        padding = b"X" * padding_length
        ciphertext_a = oracle(padding + b"A" * (2 * BLOCK_SIZE))
        ciphertext_b = oracle(padding + b"B" * (2 * BLOCK_SIZE))

        for start in range(0, len(ciphertext_a) - BLOCK_SIZE, BLOCK_SIZE):
            first_a = ciphertext_a[start:start + BLOCK_SIZE]
            second_a = ciphertext_a[start + BLOCK_SIZE:start + 2 * BLOCK_SIZE]
            first_b = ciphertext_b[start:start + BLOCK_SIZE]
            second_b = ciphertext_b[start + BLOCK_SIZE:start + 2 * BLOCK_SIZE]
            if first_a == second_a and first_b == second_b and first_a != first_b:
                return start, padding_length

    raise ValueError("Impossible d'aligner l'entrée après le préfixe.")


def aligned_oracle(user_input: bytes, start: int, padding_length: int) -> bytes:
    """Aligne l'entrée et retire les blocs correspondant au préfixe."""
    return oracle(b"X" * padding_length + user_input)[start:]


def find_secret_length(start: int, padding_length: int) -> int:
    """Déduit la longueur du secret au premier changement de taille chiffrée."""
    initial_length = len(aligned_oracle(b"", start, padding_length))
    for extra_length in range(1, BLOCK_SIZE + 1):
        ciphertext = aligned_oracle(b"X" * extra_length, start, padding_length)
        if len(ciphertext) != initial_length:
            return initial_length - extra_length
    raise ValueError("Impossible de déterminer la longueur du secret.")


def solve() -> bytes:
    """Aligne l'oracle, puis retrouve le secret octet par octet."""
    start, padding_length = find_alignment()
    secret_length = find_secret_length(start, padding_length)
    known_size = BLOCK_SIZE - 1
    recovered = b"A" * known_size

    for position in range(secret_length):
        block_start = (position // BLOCK_SIZE) * BLOCK_SIZE
        padding = b"A" * (known_size - position % BLOCK_SIZE)
        ciphertext = aligned_oracle(padding, start, padding_length)
        target = ciphertext[block_start:block_start + BLOCK_SIZE]

        known = recovered[-known_size:]
        for candidate in range(256):
            probe = known + bytes([candidate])
            ciphertext = aligned_oracle(probe, start, padding_length)
            if ciphertext[:BLOCK_SIZE] == target:
                recovered += bytes([candidate])
                break
        else:
            raise ValueError(f"Aucun candidat trouvé pour l'octet {position}.")

    return recovered[known_size:]


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
