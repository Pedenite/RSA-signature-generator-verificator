import argparse
import hashlib
from util.args_helper import str2bool
from util.keygen import generate
from util.byte_converter import bytes_to_str

parser = argparse.ArgumentParser(description='Cifra e decifra usando o RSA.', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('mensagem', type=argparse.FileType('rb'), help='Arquivo com a mensagem a ser cifrada/decifrada')
# parser.add_argument('-k', nargs='?', type=argparse.FileType('rb'), help='Arquivo com a chave de criptografia. Se não informado, será gerada uma chave automaticamente que será salva no arquivo \'keys/key[tamanho da chave]\'', metavar='chave')
# parser.add_argument('-o', type=argparse.FileType('wb'), help='Arquivo de saída', metavar='output', required=True)
parser.add_argument('-d', nargs='?', type=str2bool, const=True, default=False, help='Especifica que a mensagem deve ser decifrada na execução (padrão: cifrar)', metavar='decifrar')

args = parser.parse_args()

m = 0
with args.mensagem as f:
    byte = f.read(1)
    while byte != b"":
        m <<= 8
        m |= ord(byte)
        byte = f.read(1)

key_pub, key = generate()

cifra = pow(m, key_pub[1], key_pub[0])
print(bytes_to_str(cifra))

decifra = pow(cifra, key[0], key[1]*key[2])
print(bytes_to_str(decifra))

hash_msg = hashlib.sha3_256(bytes_to_str(m).encode("utf-8")).hexdigest()
hash_deciphered = hashlib.sha3_256(bytes_to_str(decifra).encode("utf-8")).hexdigest()

print(hash_msg == hash_deciphered)
