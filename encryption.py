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
            # Creates new file and removes the old one
            with open(file_name + ".enc", 'wb') as fo:
                [fo.write(x) for x in (cipher.nonce, tag, ciphertext)]
                fo.close()
            os.remove(file_name)

            # Updates the files array
            count = 0
            for i in files:
                if file_name == i:
                    blankFiles[count] = file_name + ".enc"
                count += 1

            # Updates the filesList array
            count = 0
            for i in filesList:
                if file_name == i:
                    blankFilesList[count] = file_name + ".enc"
                count += 1
        elif savePath != []:
            lastSlash = [pos for pos, char in enumerate(file_name) if char == "/" or char == "\\"]
            newPath = savePath[0] + "/" + file_name[lastSlash[-1] + 1:]
            newPath += ".enc"

            with open(newPath, 'wb') as fo:
                [fo.write(x) for x in (cipher.nonce, tag, ciphertext)]
                fo.close()
            os.remove(file_name)

            # Updates the files arrays
            count = 0
            for i in files:
                if file_name == i:
                     blankFiles[count] = newPath
                count += 1

            # Updates the filesList array
            count = 0
            for i in filesList:
                if file_name == i:
                    blankFilesList[count] = newPath
                count += 1


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

        if savePath == []:
            # Creates a new file and removes the old one
            with open(file_name[:-4], 'wb') as fo:
                fo.write(dec)
                fo.close()
            os.remove(file_name)

            # Updates the files arrays
            count = 0
            for i in files:
                if file_name == i:
                     blankFiles[count] = file_name[:-4]
                count += 1

            # Updates the filesList array
            count = 0
            for i in filesList:
                if file_name == i:
                    blankFilesList[count] = file_name[:-4]
                count += 1
        elif savePath != []:
            lastSlash = [pos for pos, char in enumerate(file_name) if char == "/" or char == "\\"]
            newPath = savePath[0] + "/" + file_name[lastSlash[-1] + 1:]
            newPath = newPath[:-4]

            with open(newPath, 'wb') as fo:
                fo.write(dec)
                fo.close()
            os.remove(file_name)

            # Updates the files arrays
            count = 0
            for i in files:
                if file_name == i:
                     blankFiles[count] = newPath
                count += 1

            # Updates the filesList array
            count = 0
            for i in filesList:
                if file_name == i:
                    blankFilesList[count] = newPath
                count += 1


def generate_key(password):
    key = hashlib.sha256(password.encode('utf-8')).digest()
    return key