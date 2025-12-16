import random

class RSACipher:
    def __init__(self, key=None):

        self.p = 61
        self.q = 53
        self.n = self.p * self.q                 # Modulus
        self.phi = (self.p - 1) * (self.q - 1)   # Euler's Totient
        
    
        self.e = self._find_public_key()
        
   
        self.d = self._mod_inverse(self.e, self.phi)

    def _gcd(self, a, b):
        while b:
            a, b = b, a % b
        return a

    def _find_public_key(self):
        e = 17
        while self._gcd(e, self.phi) != 1:
            e += 2
        return e

    def _mod_inverse(self, a, m):
      
        m0 = m
        y = 0
        x = 1
        if m == 1: return 0
        while a > 1:
            q = a // m
            t = m
            m = a % m
            a = t
            t = y
            y = x - q * y
            x = t
        if x < 0: x = x + m0
        return x

    def encrypt(self, text: str) -> str:
        if not text: return ""
      
        try:
            cipher_list = [str(pow(ord(char), self.e, self.n)) for char in text]
            return ",".join(cipher_list)
        except:
            return ""

    def decrypt(self, text: str) -> str:
        if not text: return ""
       
        try:
            cipher_list = text.split(',')
            plain_text = ""
            for code in cipher_list:
                m = pow(int(code), self.d, self.n)
                plain_text += chr(m)
            return plain_text
        except:
            return "RSA Hatası"