import random
import base64
import os
from rsa.keys import DEFAULT_SIZE
from util.byte_converter import bytes_to_str
from util.byte_converter import bytes_to_arr

BLOCK_SIZE = 128

def generate_key():
    key = []
    n = random.randint(0, 0xffffffffffffffffffffffffffffffff)
    for i in range(int(BLOCK_SIZE/8)):
        key.append(n&0xff)
        n >>= 8

    return key

def save_keys(key, key_ciphered):
    id_key = len([x for x in os.listdir('../keys') if x.startswith('session_')])//2
    filename = f'session_{id_key}'
    with open(f"../keys/{filename}.pub", "w") as f:
        res = bytes_to_arr(key_ciphered)

        out = base64.b64encode(bytes(res))
        f.write(out.decode("utf-8"))

    with open(f'../keys/{filename}', "w") as f:
        res = base64.b64encode(bytes(key)).decode("utf-8")
        f.write(res)

    print("A chave de sessão foi salva no arquivo", filename, "da pasta keys")

def parse_key(key):
    def is_valid(key):
        return len(key) == BLOCK_SIZE/8

    if is_valid(key):
        return key
    else:
        raise Exception(f"Chave inválida! As chaves devem ter exatamente {BLOCK_SIZE} bits de tamanho")
