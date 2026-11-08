from set1.challenge6.hamming_distance import distance

def test_hamming_distance():
    assert distance(b"this is a test", b"wokka wokka!!!") == 37
