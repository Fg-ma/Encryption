from itertools import chain
from Crypto.Cipher import AES
import hashlib
import os
import os.path

from vars import *


class encryptor:
    def __init__(self, key) -> None:
        self.key = key


    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return ciphertext, tag, cipher


    def encrypt_file(self, file_name):
        
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()

        ciphertext, tag, cipher = self.encrypt(plaintext)

        if savePath == []:
            with open(file_name + ".enc", 'wb') as fo:
                [fo.write(x) for x in (cipher.nonce, tag, ciphertext)]
                fo.close()
            os.remove(file_name)
        elif savePath != []:
            lastSlash = [pos for pos, char in enumerate(file_name) if char == "/"]
            print(file_name[lastSlash[-1]:])
            newPath = savePath[0] + "/" + file_name[lastSlash[-1]:]
            print(newPath)

            with open(newPath + ".enc", 'wb') as fo:
                [fo.write(x) for x in (cipher.nonce, tag, ciphertext)]
                fo.close()
            os.remove(file_name)



    def decrypt(self, ciphertext, nonce, tag):

        cipher = AES.new(self.key, AES.MODE_EAX, nonce)

        try:
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.rstrip(b"\0")
        except ValueError:
            print("Key incorrect or message corrupted")


    def decrypt_file(self, file_name):

        with open(file_name, 'rb') as fo:
            nonce, tag, ciphertext = [fo.read(x) for x in (16, 16, -1)]
        dec = self.decrypt(ciphertext, nonce, tag)

        if (dec == None):
            exit()

        os.rename(file_name, file_name[:-4])
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
            fo.close()


def generate_key(password):
    key = hashlib.sha256(password.encode('utf-8')).digest()
    return key