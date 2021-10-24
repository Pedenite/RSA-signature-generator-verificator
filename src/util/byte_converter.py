def bytes_to_str(n):
    res = ""
    while n > 0:
        res = chr(n & 0xff) + res
        n >>= 8

    return res

def str_to_bytes(s):
    res = 0
    for c in s:
        res <<= 8
        res |= ord(c)

    return res

def bytes_to_arr(n):
    res = []
    while n > 0:
        res.insert(0, n & 0xff)
        n >>= 8

    return res

def arr_to_bytes(a):
    res = 0
    for c in a:
        res <<= 8
        res |= c

    return res
