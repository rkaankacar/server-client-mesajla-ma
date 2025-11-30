import hashlib

class DSACipher:
    def __init__(self, key=None):
       
        self.q = 11  # Asal bölen
        self.p = 23  # Asal modül 
        self.g = 4   # Üreteç 
        
        #  0 < x < q
        self.x = 3  
        
       
        self.y = pow(self.g, self.x, self.p)

    def _hash(self, text):
       
        h = hashlib.sha1(text.encode()).hexdigest()
        return int(h, 16)

    def encrypt(self, text: str) -> str:
      
        if not text: return ""
        
     
        k = 4 
        
        
        r = pow(self.g, k, self.p) % self.q
        
       
        k_inv = pow(k, -1, self.q)
        hm = self._hash(text)
        
        s = (k_inv * (hm + self.x * r)) % self.q
        
      
        return f"{text}||{r},{s}"

    def decrypt(self, text: str) -> str:
      
        if not text or "||" not in text: return "Geçersiz Format"
        
        try:
            original_msg, signature = text.split("||")
            r_str, s_str = signature.split(',')
            r = int(r_str)
            s = int(s_str)
            
         
            w = pow(s, -1, self.q)
            hm = self._hash(original_msg)
            
          
            u1 = (hm * w) % self.q
            
       
            u2 = (r * w) % self.q
            
            
            val1 = pow(self.g, u1, self.p)
            val2 = pow(self.y, u2, self.p)
            v = (val1 * val2) % self.p % self.q
            
            if v == r:
                return f"{original_msg} (İmza Doğrulandı ✅)"
            else:
                return "SAHTE İMZA! (Doğrulama Başarısız ❌)"
        except:
            return "DSA Doğrulama Hatası"