import argparse
import hashlib
import base64
import os, sys
from rsa.keys import generate_pair
from rsa.keys import parse_key
import rsa.cipher as rsa
import aes.keys as aeskey
import aes.cipher as aes
from util.args_helper import str2bool
from util.byte_converter import bytes_to_str
from util.byte_converter import bytes_to_arr
from util.byte_converter import arr_to_bytes

parser = argparse.ArgumentParser(description='Cifra e decifra usando o RSA.', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('mensagem', type=argparse.FileType('rb'), help='Arquivo com a mensagem a ser cifrada/decifrada')
parser.add_argument('-k', nargs='?', type=argparse.FileType('r'), help='Arquivo com a chave pública ou privada (a depender do modo usado). Se não informado, serão geradas as chaves automaticamente que serão salvas no arquivo \'keys/key_[id incremental]\'', metavar='chave')
parser.add_argument('-s', nargs='?', type=argparse.FileType('r'), help='Arquivo com a chave de sessão para a cifração simétrica da mensagem. Se não informado, será gerada no arquivo \'keys/session_[id incremental]\'', metavar='session')
parser.add_argument('-o', type=argparse.FileType('wb'), help='Arquivo de saída', metavar='output', required=True)
parser.add_argument('-d', nargs='?', type=str2bool, const=True, default=False, help='Especifica que a mensagem deve ser decifrada na execução (padrão: cifrar)', metavar='decifrar')

args = parser.parse_args()

os.chdir(os.path.dirname(sys.argv[0]))

m = 0
m_blocks = []
with args.mensagem as f:
    byte = f.read(1)
    while byte != b"":
        m_blocks.append(ord(byte))
        m <<= 8
        m |= ord(byte)
        byte = f.read(1)

pswd = session = key_pub = None
if args.k == None:
    if args.d:
        print("Para verificar a assinatura, é necessário passar a chave pública!")
        exit()

    key_pub, key = generate_pair()
    pswd = key_pub if args.d else key
else:
    try:
        pswd = parse_key(args.k, args.d)
    except Exception as e:
        print(e)
        exit()

if args.s == None:
    if args.d:
        print("Para decifrar, é necessário passar a chave de sessão")

    session = aeskey.generate_key()
else:
    try:
        content = ""
        with args.s as f:
            content = base64.b64decode(f.read())
        
        cont_bytes = [x for x in content]

        if args.d:
            content = arr_to_bytes(cont_bytes)

            decripted = rsa.decrypt(content, pswd)
            cont_bytes = bytes_to_arr(decripted)

        session = aeskey.parse_key(cont_bytes)

    except Exception as e:
        print(e)
        exit()

res = aes.Cipher(m_blocks, session.copy())

if not args.d and args.s == None:
    secret = rsa.encrypt(arr_to_bytes(session), pswd)
    aeskey.save_keys(session, secret)


file = args.mensagem if args.d else args.o
file_attr = file.name.split(".")
filename = ".".join(file_attr[:-1])
file_ext = file_attr[-1]

def generateSign():
    blocks = []
    for block in res.blocks:
        blocks += block
    msg_hash = hashlib.sha3_256(bytes(blocks))
    with open(f"../{filename}_sign.{file_ext}", "w") as f:
        f.write(base64.b64encode(msg_hash.digest()).decode("utf-8"))

def verifySign():
    with open(f"../{filename}_sign.{file_ext}", "r") as f:
        hashOfMsg = f.read()
    msg_hash = hashlib.sha3_256(bytes(m_blocks))
    print("A assinatura é válida!" if hashOfMsg == base64.b64encode(msg_hash.digest()).decode("utf-8") else "A assinatura é inválida!")

if args.d:
    verifySign()
else:
    generateSign()

with args.o as f:
    blocks = []
    for block in res.blocks:
        blocks += block

    if args.d:
        for i in range(15):
            if blocks[-1] == ord('{'):
                blocks.pop()
            else:
                break

    f.write(bytes(blocks))
