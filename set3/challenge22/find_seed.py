import random
import time

from set3.challenge21.generateur import MTI19937


def setup() -> tuple[int, int, int]:
    current_time = int(time.time())
    seed = current_time + random.randint(4, 100)
    output = MTI19937(seed).random_number()
    reception = seed + random.randint(4, 100)
    return output, reception, seed
