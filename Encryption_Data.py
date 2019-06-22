#!/usr/bin/env python

import base64

from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
#unpad = lambda s : s[0:-ord(s[-1])] # python2
unpad = lambda s : s[0:-(s[-1])] # python3



class AESCipher:

    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        res = base64.b64encode( iv + cipher.encrypt( raw ) )
        return res

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        res = unpad(cipher.decrypt( enc[16:] ))
        print(res)
        #return unpad(cipher.decrypt( enc[16:] ))
        return res


# cipher = AESCipher('jts/jpipe/v_0_0_1/data/dregister')
# encrypted = cipher.encrypt('{"username": "807D3AEBE358", "password": "807D3AEBE358"}')
# decrypted = cipher.decrypt(encrypted)
# print ("encrypted : ",encrypted)
# print ("decrypted : ",decrypted)