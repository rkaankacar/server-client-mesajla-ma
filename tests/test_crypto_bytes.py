import unittest
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.encryption.aes_library import AESLibraryCipher
from core.encryption.des_library import DESLibraryCipher
from Crypto.Random import get_random_bytes

class TestCryptoBytes(unittest.TestCase):
    def test_aes_bytes(self):
        key = get_random_bytes(16)
        cipher = AESLibraryCipher(key)
        
        # Test binary data (including null bytes)
        original_data = b"Hello World \x00\xFF Binary Data"
        encrypted = cipher.encrypt_bytes(original_data)
        
        self.assertNotEqual(original_data, encrypted)
        self.assertIsInstance(encrypted, bytes)
        
        decrypted = cipher.decrypt_bytes(encrypted)
        self.assertEqual(original_data, decrypted)

    def test_des_bytes(self):
        key = get_random_bytes(8)
        cipher = DESLibraryCipher(key)
        
        original_data = b"DES Test \x00\xFF Bytes"
        encrypted = cipher.encrypt_bytes(original_data)
        
        self.assertNotEqual(original_data, encrypted)
        self.assertIsInstance(encrypted, bytes)
        
        decrypted = cipher.decrypt_bytes(encrypted)
        self.assertEqual(original_data, decrypted)

    def test_aes_key_handling(self):
        # Test string key
        cipher_str = AESLibraryCipher("MySixteenByteKey")
        self.assertEqual(len(cipher_str.key), 16)
        
        # Test bytes key
        key_bytes = get_random_bytes(16)
        cipher_bytes = AESLibraryCipher(key_bytes)
        self.assertEqual(cipher_bytes.key, key_bytes)

if __name__ == '__main__':
    unittest.main()
