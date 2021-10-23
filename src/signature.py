import argparse
import hashlib
import base64
import os, sys
from rsa.keys import generate_pair
from rsa.keys import parse_key
import rsa.cipher as rsa
from util.args_helper import str2bool
from util.byte_converter import bytes_to_str

parser = argparse.ArgumentParser(description='Cifra e decifra usando o RSA.', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('mensagem', type=argparse.FileType('rb'), help='Arquivo com a mensagem a ser cifrada/decifrada')
parser.add_argument('-k', nargs='?', type=argparse.FileType('r'), help='Arquivo com a chave pública ou privada (a depender do modo usado). Se não informado, serão geradas as chaves automaticamente que serão salvas no arquivo \'keys/key_[id incremental]\'', metavar='chave')
parser.add_argument('-o', type=argparse.FileType('wb'), help='Arquivo de saída', metavar='output', required=True)
parser.add_argument('-d', nargs='?', type=str2bool, const=True, default=False, help='Especifica que a mensagem deve ser decifrada na execução (padrão: cifrar)', metavar='decifrar')

args = parser.parse_args()

os.chdir(os.path.dirname(sys.argv[0]))

m = 0
with args.mensagem as f:
    byte = f.read(1)
    while byte != b"":
        m <<= 8
        m |= ord(byte)
        byte = f.read(1)

pswd = key_pub = key = None
if args.k == None:
    if args.d:
        print("Para decifrar, é necessário passar uma chave!")
        exit()

    key_pub, key = generate_pair()
    pswd = key if args.d else key_pub
else:
    try:
        pswd = parse_key(args.k, args.d)
    except Exception as e:
        print(e)
        exit()

res = rsa.decrypt(m, pswd) if args.d else rsa.encrypt(m, pswd)

with args.o as f:
    arr = []
    temp = res
    while temp > 0:
        arr.insert(0, temp & 0xff)
        temp >>= 8

    f.write(bytes(arr))

file = args.mensagem if args.d else args.o
file_attr = file.name.split(".")
filename = ".".join(file_attr[:-1])
file_ext = file_attr[-1]

if args.d:
    old_hash = ""
    hash_msg = hashlib.sha3_256(bytes_to_str(res).encode("utf-8")).hexdigest()
    print(hash_msg)
    with open(f"../{filename}_hash.{file_ext}", "r") as f:
        old_hash = base64.b64decode(f.read()).decode("utf-8")
    
    print("O hash da mensagem decifrada é equivalente ao encontrado no arquivo!" if old_hash == hash_msg else "Os hashs se diferem!")
else:
    hash_msg = hashlib.sha3_256(bytes_to_str(m).encode("utf-8")).hexdigest()
    print(f"hash da mensagem armazenado no arquivo {filename}_hash.{file_ext}", hash_msg, sep='\n')
    with open(f"../{filename}_hash.{file_ext}", "w") as f:
        f.write(base64.b64encode(hash_msg.encode("utf-8")).decode("utf-8"))

