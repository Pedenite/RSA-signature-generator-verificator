import hashlib
import base64
import rsa.cipher as rsa
from util.byte_converter import arr_to_bytes
from util.byte_converter import bytes_to_arr

def generate(filename, msg, key):
    msg_hash = hashlib.sha3_256(bytes(msg))
    sign = rsa.encrypt(arr_to_bytes([x for x in msg_hash.digest()]), key)

    with open(f"../{filename}_sign", "w") as f:
        f.write(base64.b64encode(bytes(bytes_to_arr(sign))).decode("utf-8"))

def verify(filename, cipher, key):
    signature = ''
    with open(f"../{filename}_sign", "r") as f:
        signature = base64.b64decode(f.read())

    extracted_sign = arr_to_bytes([x for x in signature])
    original_hash = rsa.decrypt(extracted_sign, key)

    msg_hash = hashlib.sha3_256(bytes(cipher)).digest()
    print("A assinatura é válida!" if original_hash == arr_to_bytes([x for x in msg_hash]) else "A assinatura é inválida!")
