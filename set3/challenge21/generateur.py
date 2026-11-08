from set3.challenge21.tempering import temper


class MTI19937:
    def __init__(self, seed: int) -> None:
        self.state = [0] * 624
        self.state[0] = seed & 0xFFFFFFFF
        for i in range(1, 624):
            previous = self.state[i - 1]
            self.state[i] = ((previous ^ (previous >> 30)) * 1812433253 + i) & 0xFFFFFFFF
        self.index = 624

    def twist(self) -> None:
        for i in range(624):
            u = (self.state[i] & 0x80000000) | (self.state[(i + 1) % 624] & 0x7FFFFFFF)
            v = u >> 1
            if u & 1:
                v ^= 0x9908B0DF
            self.state[i] = self.state[(i + 397) % 624] ^ v
        self.index = 0

    def random_number(self) -> int:
        if self.index >= 624:
            self.twist()
        result = temper(self.state[self.index])
        self.index += 1
        return result
