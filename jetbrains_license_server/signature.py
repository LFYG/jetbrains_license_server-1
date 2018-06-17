import binascii
import os

from Cryptodome.Hash import MD5
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_FILE = os.path.join(BASE_DIR, 'private.pem')


def sign(data):
    key = open(KEY_FILE, 'r').read()
    rsa_key = RSA.import_key(key)
    signer = pkcs1_15.new(rsa_key)
    digest = MD5.new()
    digest.update(data.encode('utf8'))
    signature = signer.sign(digest)
    return binascii.hexlify(signature).decode()
