'''
Keys for digital signatures and integrated encryptions.

Usage:
>>> k1 = ECKeys()
>>> k2 = ECKeys()
>>> k1.load(k2.export())
>>> k2.load(k1.export())
>>> k2.verify(b'data', k1.sign(b'data'))
True
>>> k1.secret() == k2.secret()
True
'''

from ecdsa import (
    SigningKey,
    VerifyingKey, 
    ECDH, 
    NIST256p,
    BadSignatureError
    )

from blowcurve import BlowcurveError

__all__ = ['MissingRemoteKey', 'ECPrivateKey', 'ECPublicKey', 'ECKeys']

class MissingRemoteKey(BlowcurveError):
    'Exception when no remote key is specified.'
    def __init__(self):
        super().__init__("remote key not loaded yet.")

class ECPrivateKey:
    'The private key for signing and decrypting.'
    def __init__(self):
        self._key = SigningKey.generate(NIST256p)
    def sign(self, data):
        'Signs the data.'
        return self._key.sign(data)
    def exportKey(self):
        'Export the key as hex string. (DER)'
        return self._key.to_der().hex()
    def publicKey(self):
        'Gets the public key of this instance.'
        return ECPublicKey(self._key.get_verifying_key())

class ECPublicKey:
    'The public key for verifying and encrypting.'
    def __init__(self, key):
        'For internal use. Do not call directly. Use ECPrivateKey.publicKey or importKey instead.'
        self._key = key
    @staticmethod
    def importKey(data):
        'Import a key from der or hex string.'
        if isinstance(data, str):
            data = bytes.fromhex(data)
        if not isinstance(data, bytes):
            raise TypeError("Invalid data type.")
        return ECPublicKey(VerifyingKey.from_der(data))
    def verify(self, data, signature):
        'Verifies a signature.'
        try:
            self._key.verify(signature, data)
            return True
        except BadSignatureError:
            return False
    def exportKey(self):
        'Export the key as hex string. (DER)'
        return self._key.to_der().hex()
    def exportString(self):
        'Export the key as byte string.'
        return self._key.to_string()

class ECKeys:
    'Represents a EC key pair.'
    def __init__(self):
        self._privateKey = ECPrivateKey()
        self._publicKey = self._privateKey.publicKey()
        self._remoteKey = None
    def load(self, key):
        'Loads a remote public key.'
        self._remoteKey = ECPublicKey.importKey(key)
    def _load(self, key):
        'Loads a remote public key. For internal use.'
        self._remotekey = key
    def secret(self):
        'Gets the shared secret.'
        if not self._remoteKey:
            raise MissingRemoteKey
        ecdh = ECDH(NIST256p, self._privateKey._key, self._remoteKey._key)
        return ecdh.generate_sharedsecret_bytes()
    def ephemeral(self, ephemeral=None):
        'Create or decapsulate a ephemeral key.'
        if not self._remoteKey:
            raise MissingRemoteKey
        if not ephemeral: # request to generate one
            eph_key = ECPrivateKey()
            ecdh = ECDH(NIST256p, eph_key._key, self._remoteKey._key)
            return eph_key.publicKey().exportString(), ecdh.generate_sharedsecret_bytes()
        else: # decapsulate key
            eph_key = ECPublicKey(VerifyingKey.from_string(ephemeral, NIST256p))
            ecdh = ECDH(NIST256p, self._privateKey._key, eph_key._key)
            return ecdh.generate_sharedsecret_bytes()
    def sign(self, data):
        'Signs the data with local private key.'
        return self._privateKey.sign(data)
    def verify(self, data, signature):
        'Verifies the data with remote public key.'
        if not self._remoteKey:
            raise MissingRemoteKey
        return self._remoteKey.verify(data, signature)
    def export(self):
        'Export the local public key.'
        return self._publicKey.exportKey()