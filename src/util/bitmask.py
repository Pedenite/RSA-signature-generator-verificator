def create_mask(n):
    res = 0
    for i in range(n):
        res <<= 1
        res |= 1

    return res
