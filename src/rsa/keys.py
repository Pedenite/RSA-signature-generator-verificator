import os
import base64
import math
from util.primes import generate_prime_number
from util.byte_converter import bytes_to_str
from util.byte_converter import str_to_bytes

DEFAULT_SIZE = 2048

def generate_pair(size=DEFAULT_SIZE):
    primes_size = size >> 1
    p = generate_prime_number(primes_size)
    q = generate_prime_number(primes_size)

    n = p*q
    phi = (p-1) * (q-1)
    e = generate_prime_number(primes_size >> 1)
    while math.gcd(e, n) != 1:
        e = generate_prime_number(primes_size >> 1)

    d = pow(e, -1, phi)     # multiplicative inverse

    public = [n, e]
    private = [d, p, q]

    store_keys(public, private, size)

    return public, private

def store_keys(pub, priv, size=DEFAULT_SIZE):
    def generate_file(path, key):
        with open(path, "w") as f:
            res = ""
            for n in key:
                sn = bytes_to_str(n)
                while len(sn) < size/8:
                    sn = chr(0) + sn

                res += sn

            out = base64.b64encode(res.encode("utf-8"))
            f.write(out.decode("utf-8"))

    id_key = len([x for x in os.listdir('../keys') if x.startswith('key_')])//2
    filename = f'key_{id_key}'

    generate_file(f'../keys/{filename}.pub', pub)
    generate_file(f'../keys/{filename}', priv)
    print(f'a chave publica foi gerada no diretorio keys/{filename}.pub')
    print(f'a chave privada foi gerada no diretorio keys/{filename}')

def parse_key(file, decod=False, size=DEFAULT_SIZE):
    key = None
    with file as f:
        b64 = f.read()
        content = base64.b64decode(b64).decode("utf-8")
        key = [content[i:i+size//8] for i in range(0, len(content), size//8)]

    if decod and len(key) == 2 or not decod and len(key) == 3:
        res = []
        for k in key:
            res.append(str_to_bytes(k))

        return res
    else:
        mode = "pública para decifrar" if decod else "privada para cifrar"
        raise Exception(f"Chave inválida! Para a assinatura digital, favor usar a chave {mode}!")
