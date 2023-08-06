from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
import hashlib
from Crypto import Random

BLOCK_SIZE = 16


def pad(size):
    return size + (BLOCK_SIZE - len(size) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(size) % BLOCK_SIZE)


def un_pad(size):
    return size[:-ord(size[len(size) - 1:])]


class Necrypt:
    def __init__(self, rsa_key_size=2048, aes_key=''):
        self._rsa_key = RSA.generate(rsa_key_size)
        self._aes_key = hashlib.sha256(aes_key.encode()).digest()

    @property
    def aes_key(self):
        return self._aes_key

    @aes_key.setter
    def aes_key(self, aes_key):
        self._aes_key = hashlib.sha256(aes_key.encode()).digest()

    def encrypt(self, plain):
        plain = pad(b64encode(plain.encode()).decode())
        iv = Random.new().read(AES.block_size)
        aes_cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        aes_b64encoded_cipher = b64encode(iv + aes_cipher.encrypt(plain.encode()))
        rsa_cipher = PKCS1_OAEP.new(self._rsa_key)
        return b64encode(rsa_cipher.encrypt(aes_b64encoded_cipher))

    def decrypt(self, aes_cipher):
        rsa_cipher = PKCS1_OAEP.new(self._rsa_key)
        rsa_decrypted_b64decoded_cipher = b64decode(rsa_cipher.decrypt(b64decode(aes_cipher)))
        iv = rsa_decrypted_b64decoded_cipher[:BLOCK_SIZE]
        aes_cipher = AES.new(self._aes_key, AES.MODE_CBC, iv)
        return b64decode(un_pad(aes_cipher.decrypt(rsa_decrypted_b64decoded_cipher[BLOCK_SIZE:]))).decode('utf8')

    def sign(self, plain):
        return pkcs1_15.new(self._rsa_key).sign(SHA256.new(plain))

    def verify(self, plain, signature):
        return pkcs1_15.new(self._rsa_key).verify(SHA256.new(plain), signature)

    def get_finger_print(self):
        pass
