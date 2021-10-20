def bytes_to_str(n):
    res = ""
    while n > 0:
        res = chr(n & 0xff) + res
        n >>= 8

    return res