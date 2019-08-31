from Crypto.PublicKey import RSA
import Crypto.Random
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import binascii
import json

class Wallet:
    def __init__(self):
        self.private_key ,self.public_key = self.generate_keys()

    def generate_keys(self):
        private_key = RSA.generate(1024,Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format="DER")).decode('ascii'),binascii.hexlify(public_key.exportKey(format="DER")).decode('ascii'))

    def signature(self , data):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        message = SHA256.new(data.encode('utf8'))
        signature = signer.sign(message)
        return binascii.hexlify(signature).decode('ascii')

    def verify(data , publickey , signature):
        public_key = RSA.importKey(binascii.unhexlify(publickey))
        verifier = PKCS1_v1_5.new(public_key)
        message = SHA256.new((json.dumps(data)).encode('utf8'))
        return verifier.verify(message ,binascii.unhexlify(signature))
