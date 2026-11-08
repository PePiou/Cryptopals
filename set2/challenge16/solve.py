from set2.challenge10.solution import xor
from set2.challenge16.context import BLOCK_SIZE, PREFIX, encrypt_user_data, is_admin


def solve() -> bool:
    """Injecte le marqueur admin en modifiant le bloc chiffré précédent."""
    target = b";admin=true;"
    known_block = b"A" * BLOCK_SIZE
    target_block = b"A" * (BLOCK_SIZE - len(target)) + target

    # Aligner un bloc de A contrôlé juste après le préfixe.
    prefix_size = len(PREFIX.encode())
    alignment_size = -prefix_size % BLOCK_SIZE
    user_input = "A" * alignment_size + known_block.decode("ascii")
    ciphertext = encrypt_user_data(user_input)
    block_start = prefix_size + alignment_size

    # En CBC, appliquer ce XOR au bloc précédent transforme A...A en cible.
    previous_start = block_start - BLOCK_SIZE
    previous_block = ciphertext[previous_start:block_start]
    modified_block = xor(previous_block, xor(known_block, target_block))
    forged_ciphertext = (
        ciphertext[:previous_start] + modified_block + ciphertext[block_start:]
    )
    return is_admin(forged_ciphertext)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
