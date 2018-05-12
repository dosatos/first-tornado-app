# coding: utf-8
from __future__ import unicode_literals
import base64
import os

import six
from Crypto import Random
from Crypto.PublicKey import RSA


class PublicKeyFileExists(Exception): pass


class RSAEncryption(object):
    PRIVATE_KEY_FILE_PATH = 'keys/private_key.bin'
    PUBLIC_KEY_FILE_PATH = 'keys/public_key.bin'

    def encrypt(self, message):
        public_key = self._get_public_key()
        public_key_object = RSA.importKey(public_key)
        random_phrase = 'M'
        encrypted_message = public_key_object.encrypt(self._to_format_for_encrypt(message), random_phrase)[0]
        # use base64 for save encrypted_message in database without problems with encoding
        return base64.b64encode(encrypted_message)

    def decrypt(self, encoded_encrypted_message):
        encrypted_message = base64.b64decode(encoded_encrypted_message)
        private_key = self._get_private_key()
        private_key_object = RSA.importKey(private_key)
        # print("PRIVATE KEY OBJECT: ", private_key_object)
        # print(encrypted_message)
        decrypted_message = private_key_object.decrypt(encrypted_message)
        return six.text_type(decrypted_message, encoding='utf8')

    def generate_keys(self):
        """Be careful rewrite your keys"""
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator)
        private, public = key.exportKey(), key.publickey().exportKey()

        if os.path.isfile(self.PUBLIC_KEY_FILE_PATH):
            raise PublicKeyFileExists('Public Key File already exists, please delete it first.')
        self.create_directories()

        with open(self.PRIVATE_KEY_FILE_PATH, 'wb') as private_file:
            private_file.write(private)
        with open(self.PUBLIC_KEY_FILE_PATH, 'wb') as public_file:
            public_file.write(public)
        return private, public

    def create_directories(self, for_private_key=True):
        public_key_path = self.PUBLIC_KEY_FILE_PATH.rsplit('/', 1)[0]
        if not os.path.exists(public_key_path):
            os.makedirs(public_key_path)
        if for_private_key:
            private_key_path = self.PRIVATE_KEY_FILE_PATH.rsplit('/', 1)[0]
            if not os.path.exists(private_key_path):
                os.makedirs(private_key_path)

    def _get_public_key(self):
        """run generate_keys() before get keys """
        with open(self.PUBLIC_KEY_FILE_PATH, 'rb') as _file:
            return _file.read()

    def _get_private_key(self):
        """run generate_keys() before get keys """
        if os.path.isfile(self.PRIVATE_KEY_FILE_PATH):
	        with open(self.PRIVATE_KEY_FILE_PATH, 'rb') as _file:
	            return _file.read()

    def _to_format_for_encrypt(self, value):
        if isinstance(value, int):
            return six.binary_type(value)
        for str_type in six.string_types:
            if isinstance(value, str_type):
                return value.encode('utf8')
        if isinstance(value, six.binary_type):
            return value


def salt_string(string):
	salt = "!?!zP0"
	return string + salt


def desalt_string(salted_string):
	if salted_string[-desalt:] == "!?!zP0":
		desalt = len("!?!zP0")
		return salted_string[:-desalt]
	return "Wrong salt!"

# if __name__ == "__main__":
# 	rsa = RSAEncryption()
# 	rsa.generate_keys()