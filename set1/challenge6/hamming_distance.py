def bytes_to_bits(bytes_input: bytes) -> list[int]:
    return [int(bit) for byte in bytes_input for bit in f"{byte:08b}"]


def string_to_bits(s: str) -> list[int]:
    return bytes_to_bits(s.encode("utf-8"))


def distance(s1: bytes, s2: bytes) -> int:
    if len(s1) != len(s2):
        raise ValueError("Les deux blocs doivent avoir la même longueur.")
    distance = 0
    s1, s2 = bytes_to_bits(s1), bytes_to_bits(s2)
    N = len(s1)
    for i in range(N):
        if s1[i] != s2[i]:
            distance += 1
    return distance


def average_distance(bytes_input: bytes, keysize: int) -> float:
    s0, s1, s2, s3 = [
        bytes_input[i * keysize:(i + 1) * keysize] for i in range(4)
    ]
    return (distance(s0,s1)+distance(s0,s2)+
            distance(s0,s3)+distance(s1,s2)+
            distance(s1,s3)+distance(s2,s3))/(6 * keysize)
