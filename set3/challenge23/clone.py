from set3.challenge21.generateur import MTI19937

SEED = 1235676576765

def untemper(x: int) -> int:
    x &= 0xFFFFFFFF
    x ^= x >> 18
    y = x
    for _ in range(2):
        x = y ^ ((x << 15) & 0xEFC60000)
    y = x
    for _ in range(4):
        x = y ^ ((x << 7) & 0x9D2C5680)
    y = x
    for _ in range(2):
        x = y ^ (x >> 11)
    return x

def main() -> None:
    rng = MTI19937(SEED)
    clone = MTI19937(0)
    for i in range(624):
        clone.state[i] = untemper(rng.random_number())
    for _ in range(700):
        print(clone.random_number() == rng.random_number())


if __name__ == "__main__":
    main()
