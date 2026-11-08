from set3.challenge21.generateur import MTI19937


def test_reproducible_sequence() -> None:
    g1 = MTI19937(42)
    g2 = MTI19937(42)

    sequence1 = [g1.random_number() for _ in range(1000)]
    sequence2 = [g2.random_number() for _ in range(1000)]

    assert sequence1 == sequence2
    assert all(0 <= number < 2**32 for number in sequence1)


if __name__ == "__main__":
    print(MTI19937(5489).random_number())
