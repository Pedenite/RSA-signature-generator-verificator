def mat_mul(a, b):
    result = [[0],[0],[0],[0]]
    for i in range(4):
        for j in range(4):
            result[i][0] ^= mul(a[i][j], b[j][0])

    return result

def mul(a, b):
    res = 0
    for x in range(b.bit_length() + 1):
        if b & (1 << x):
            res ^= a << x

    while res.bit_length() > 8:
        res ^= 0x11b << (res.bit_length() - 9)

    return res

def rcon(n):
    res = 1
    for i in range(n):
        res = (res<<1) ^ (0x11b & -(res>>7))
    
    return res
