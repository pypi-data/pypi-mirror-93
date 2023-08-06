'''
Simple module for ECIES (Elliptic-Curve Integrated Encryption Scheme) with Blowfish symmetric encryption.
This module also provides implementation of ECDSA (Elliptic-Curve Digital Signature Algorithm) and ECDH
(Elliptic-Curve Diffie-Hellman) key exchange mechanism.

Usage:
>>> bc1 = Blowcurve()
>>> bc2 = Blowcurve()
>>> bc1.load(bc2.export())
>>> bc2.load(bc1.export())
>>> bc1.verify(b'data', bc2.sign(b'data'))
True
>>> bc2.decrypt(bc1.encrypt(b'data'))
b'data'
'''

class BlowcurveError(Exception): pass

from .keys import ECKeys
from . import crypt

__all__ = ['BlowcurveError', 'Blowcurve']

EC_PUBLIC_KEY_SIZE = 64

class Blowcurve:
    'Blowcurve main class.'
    def __init__(self):
        self._pair = ECKeys()
    def load(self, remote_key):
        'Loads a remote public key.'
        self._pair.load(remote_key)
    def sign(self, data):
        'Signs the data with local private key.'
        return self._pair.sign(data)
    def verify(self, data, signature):
        'Verifies the data with remote public key.'
        return self._pair.verify(data, signature)
    def encrypt(self, data):
        'Encrypts the data using ephermal keys.'
        ephemeral, key = self._pair.ephemeral()
        return ephemeral + crypt.encrypt(key, data)
    def decrypt(self, data):
        'Decrypts the data.'
        ephemeral, data = data[:EC_PUBLIC_KEY_SIZE], data[EC_PUBLIC_KEY_SIZE:]
        return crypt.decrypt(self._pair.ephemeral(ephemeral), data)
    def export(self):
        'Exports the key in hex string.'
        return self._pair.export()