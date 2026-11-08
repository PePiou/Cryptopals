def temper(state_value: int) -> int:
    state_value ^= state_value >> 11
    state_value ^= (state_value << 7) & 0x9D2C5680
    state_value ^= (state_value << 15) & 0xEFC60000
    state_value ^= state_value >> 18
    return state_value & 0xFFFFFFFF
