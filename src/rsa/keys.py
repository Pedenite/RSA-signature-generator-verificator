import os
import base64
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
    e = 65537               # TODO: 'e' needs to be coprime with 'phi'

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

    id_key = len(os.listdir('../keys'))//2
    filename = f'key_{id_key}'

    generate_file(f'../keys/{filename}.pub', pub)
    generate_file(f'../keys/{filename}', priv)

def parse_key(file, decod=False, size=DEFAULT_SIZE):
    key = None
    with file as f:
        b64 = f.read()
        content = base64.b64decode(b64).decode("utf-8")
        key = [content[i:i+size//8] for i in range(0, len(content), size//8)]

    if decod and len(key) == 3 or not decod and len(key) == 2:
        res = []
        for k in key:
            res.append(str_to_bytes(k))

        return res
    else:
        mode = "privada para decifrar" if decod else "pública para cifrar"
        raise Exception(f"Chave inválida! Favor usar a chave {mode}!")
