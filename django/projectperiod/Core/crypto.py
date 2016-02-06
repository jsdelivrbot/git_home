from django.conf import settings
from Crypto.Cipher import AES

import logging
import base64


logger = logging.getLogger(__name__)

class Crypto(object):
    def encrypt(self, text):
        BLOCK_SIZE = 32
        PADDING = '{'
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        cipher = AES.new(settings.AES_KEY)
        encoded = EncodeAES(cipher, text)

        return encoded

    def decrypt(self, text):
        PADDING = '{'
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        cipher = AES.new(settings.AES_KEY)
        decoded = DecodeAES(cipher, text)

        return decoded