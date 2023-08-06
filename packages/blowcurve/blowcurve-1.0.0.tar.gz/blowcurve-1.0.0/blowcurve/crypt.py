'''
API functions for Blowfish encryption schemes.
Also provides utilities for PKCS5 padding/unpadding.

Usage:
>>> pkcs5_pad(b'data', 8)
b'data\\x04\\x04\\x04\\x04'
>>> pkcs5_unpad(b'data\\x04\\x04\\x04\\x04')
b'data'
>>> key = b'mykey'
>>> decrypt(key, encrypt(key, b'data'))
b'data'
'''

from Crypto.Protocol.KDF import HKDF
from Crypto.Cipher import Blowfish
from Crypto.Hash import SHA256
from blowcurve import BlowcurveError
import os

# constants
SALT_LENGTH = 16
FISH_KEY_SIZE = 32
FISH_MODE = Blowfish.MODE_CBC

__all__ = ['encrypt', 'decrypt', 'pkcs5_pad', 'pkcs5_unpad']

class IncorrectPadding(BlowcurveError):
    def __init__(self):
        super().__init__("incorrect padding")

def pkcs5_pad(data, size):
    'Pads the specific data with provided block size.'
    padlen = size - len(data) % size
    return data + bytes((padlen,)*padlen)

def pkcs5_unpad(data):
    'Unpads the specific data.'
    data, padding = data[:-data[-1]], data[-data[-1]:]
    if padding != bytes((padding[-1],)*len(padding)): 
        raise IncorrectPadding
    return data

def get_salt_iv():
    'Randomly generates a pair of salt and initial vector.'
    return os.urandom(SALT_LENGTH), os.urandom(Blowfish.block_size)

def extract_salt_iv(data):
    'Extracts salt and vector from encrypted data.'
    salt, data = data[:SALT_LENGTH], data[SALT_LENGTH:]
    iv, data = data[:Blowfish.block_size], data[Blowfish.block_size:]
    return salt, iv, data

def derive_key(salt, key):
    'Derives a Blowfish key from specified master and salt. Uses HKDF-SHA256.'
    key = HKDF(key, FISH_KEY_SIZE, salt, SHA256)
    return key

def encrypt(key, data):
    'Encrypts the data with specific key.'
    salt, iv = get_salt_iv()
    derived = derive_key(salt, key)
    cipher = Blowfish.new(derived, FISH_MODE, iv)
    return salt+iv+cipher.encrypt(pkcs5_pad(data, Blowfish.block_size))

def decrypt(key, data):
    'Decrypts the data with specific key.'
    salt, iv, data = extract_salt_iv(data)
    derived = derive_key(salt, key)
    cipher = Blowfish.new(derived, FISH_MODE, iv)
    return pkcs5_unpad(cipher.decrypt(data))