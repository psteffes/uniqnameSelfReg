from django.conf import settings
from itsdangerous import URLSafeTimedSerializer, TimedJSONWebSignatureSerializer
import logging

logger = logging.getLogger(__name__)

import json
import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

# http://depado.markdownblog.com/2015-05-11-aes-cipher-with-python-3-x
class AESCipher(object):
    """
    A classical AES Cipher. Can use any size of data and any size of password thanks to padding.
    Also ensure the coherence and the type of the data with a unicode to byte converter.
    """
    def __init__(self, key):
        self.bs = 32
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b''.decode('utf8'))
        if isinstance(data, u_type):
            return data.encode('utf8')
        return data

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

    def encrypt(self, raw):
        raw = self._pad(AESCipher.str_to_bytes(raw))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')


def generate_confirmation_token(data):
    """
    Generate a JSONWebSignature. Used to send to the user to confirm email address
    """
    serializer = TimedJSONWebSignatureSerializer(
        settings.SECRET_KEY,
        expires_in = settings.TOKEN_EXPIRATION_SECONDS,
    )

    cipher = AESCipher(key=settings.SECRET_KEY)
    ciphertext = cipher.encrypt(json.dumps(data))

    return serializer.dumps(ciphertext, salt=settings.SECURITY_CONFIRM_SALT)
    #return serializer.dumps(data, salt=settings.SECURITY_CONFIRM_SALT)


def confirm_token(token):
    """
    Validate a JSONWebSignature. Return the json data
    """
    try:
        serializer = TimedJSONWebSignatureSerializer(
            settings.SECRET_KEY,
            expires_in = settings.TOKEN_EXPIRATION_SECONDS,
        )
        data = serializer.loads(
            token,
            salt=settings.SECURITY_CONFIRM_SALT,
        )
        cipher = AESCipher(key=settings.SECRET_KEY)
        decrypted = cipher.decrypt(data)
    except Exception as e:
        raise

    return json.loads(decrypted)

