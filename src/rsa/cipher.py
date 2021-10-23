def encrypt(msg, key):
    n = key[0]
    e = key[1]

    return pow(msg, e, n)

def decrypt(cipher, key):
    d = key[0]
    p = key[1]
    q = key[2]
    
    return pow(cipher, d, p*q)
