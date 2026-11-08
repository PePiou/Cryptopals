from set3.challenge21.generateur import MTI19937
from set3.challenge22.find_seed import setup


def test_seed_recovery() -> None:
    output, reception, expected_seed = setup()
    candidate_seed = reception
    while True:
        if output == MTI19937(candidate_seed).random_number():
            assert candidate_seed == expected_seed
            return
        candidate_seed -= 1


if __name__ == "__main__":
    test_seed_recovery()
