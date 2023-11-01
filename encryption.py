from itertools import chain
from Crypto.Cipher import AES
import hashlib
import os
import os.path

from vars import *


class encryptor:

    """
    Creates a class that can encrypt and decrypt single files inputed via a path to it,
    does this using AES encryption standard to create a cypher based on the inputed password,
    also accepts a save path for updating the paths to the new files.
    """

    def __init__(self, key) -> None:
        self.key = key


    def encrypt(self, data):

        """
        Actually encrypts the data and returns encrypted data as wells as tag and cipher
        """

        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return ciphertext, tag, cipher


    def encrypt_file(self, file_name):

        """
        Opens a decrypted file then sends the data to be encrypted in encrypt function,
        then creates a encrypted file from the encrypted data and returns an encrypted file
        (deleting the old decrypted file in the process),
        then handles updating relevant paths and variables
        """

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

        """
        Actually decrypts the data and returns decrypted data
        """

        cipher = AES.new(self.key, AES.MODE_EAX, nonce)

        try:
            plaintext = cipher.decrypt_and_verify(ciphertext, tag)
            return plaintext.rstrip(b"\0")
        except ValueError:
            print("Key incorrect or message corrupted")


    def decrypt_file(self, file_name):   

        """
        Opens a encrypted file then sends the data to be decrypted in decrypt function,
        then creates a decrypted file from the decrypted data and returns a decrypted file
        (deleting the old encrypted file in the process),
        then handles updating relevant paths and variables
        """

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

    """
    Generates a sha256 key from an inputed password the retuns the key used for encryption or decrpytion
    """

    key = hashlib.sha256(password.encode('utf-8')).digest()
    return key