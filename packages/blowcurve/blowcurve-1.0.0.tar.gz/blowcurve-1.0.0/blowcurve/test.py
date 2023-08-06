from blowcurve import Blowcurve
from .keys import ECKeys, MissingRemoteKey
from . import crypt
import unittest, os

class BlowcurveTestCase(unittest.TestCase):
    def setUp(self):
        self.bc1 = Blowcurve()
        self.bc2 = Blowcurve()
        self.bc1.load(self.bc2.export())
        self.bc2.load(self.bc1.export())
    def testSign(self):
        data = os.urandom(32)
        signature = self.bc1.sign(data)
        self.assertTrue(self.bc2.verify(data, signature), "Invalid signature for blowcurve 2")
        data = os.urandom(32)
        signature = self.bc2.sign(data)
        self.assertTrue(self.bc1.verify(data, signature), "Invalid signature for blowcurve 1")
    def testEncrypt(self):
        data = os.urandom(32)
        self.assertEqual(self.bc2.decrypt(self.bc1.encrypt(data)), data, "Encryption failed.")
        self.assertEqual(self.bc1.decrypt(self.bc2.encrypt(data)), data, "Encryption failed.")

class KeysTestCase(unittest.TestCase):
    def setUp(self):
        self.p1 = ECKeys()
        self.p2 = ECKeys()
        self.p1.load(self.p2.export())
        self.p2.load(self.p1.export())
    def testSecret(self):
        self.assertEqual(self.p1.secret(), self.p2.secret(), "Different shared secrets.")
    def testSign(self):
        data = os.urandom(32)
        signature = self.p1.sign(data)
        self.assertTrue(self.p2.verify(data, signature), "Invalid signature for keys 2")
        data = os.urandom(32)
        signature = self.p2.sign(data)
        self.assertTrue(self.p1.verify(data, signature), "Invalid signature for keys 1")
    def testNoRemoteKey(self):
        keys = ECKeys()
        self.assertRaises(MissingRemoteKey, keys.verify, None, None)

class CryptTestCase(unittest.TestCase):
    def testPad(self):
        data = os.urandom(20)
        self.assertEqual(crypt.pkcs5_pad(data, 8), data + b"\4\4\4\4", "Incorrect padding.")
        data = os.urandom(20)
        self.assertEqual(crypt.pkcs5_pad(data, 10), data + b'\n\n\n\n\n\n\n\n\n\n', "Incorrect padding.")
        data = os.urandom(20)
        self.assertEqual(crypt.pkcs5_unpad(data + b'\4\4\4\4'), data, "Incorrect unpadding.")
        data = os.urandom(20)
        self.assertRaises(crypt.IncorrectPadding, crypt.pkcs5_unpad, data + b'\3\4\3')
    def testEncrypt(self):
        data = os.urandom(20)
        salt = os.urandom(16)
        key = crypt.derive_key(salt, data)
        self.assertEqual(32, len(key), "Incorrect key length.")
        self.assertEqual(crypt.decrypt(key, crypt.encrypt(key, data)), data, "Encryption failed.")

if __name__ == '__main__':
    unittest.main()