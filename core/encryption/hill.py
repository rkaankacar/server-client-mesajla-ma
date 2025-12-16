import math

class HillCipher:
    def __init__(self, key_str: str = "HILL"):
       
        key_clean = "".join(filter(str.isalpha, key_str.upper()))
        if len(key_clean) < 4:
            key_clean = "HILL"  
        
       
        k = [ord(c) - 65 for c in key_clean[:4]]
        
      
        self.matrix = [[k[0], k[1]], [k[2], k[3]]]
        
       
        try:
            self.inverse_matrix = self._get_inverse_matrix(self.matrix)
        except ValueError:
           
            self.matrix = [[7, 8], [11, 11]] # "HILL"
            self.inverse_matrix = self._get_inverse_matrix(self.matrix)

    def _get_inverse_matrix(self, matrix):
       
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        det = det % 26
        
      
        try:
            det_inv = pow(det, -1, 26)
        except ValueError:
            raise ValueError("Bu anahtar matematiksel olarak geçersiz (Tersi alınamıyor).")

 
        m00 = (matrix[1][1] * det_inv) % 26
        m01 = (-matrix[0][1] * det_inv) % 26
        m10 = (-matrix[1][0] * det_inv) % 26
        m11 = (matrix[0][0] * det_inv) % 26
        
        return [[m00, m01], [m10, m11]]

    def _process(self, text, matrix):

        text_clean = "".join(filter(str.isalpha, text.upper()))
        
   
        if len(text_clean) % 2 != 0:
            text_clean += 'X'
            
        result = ""
       
        for i in range(0, len(text_clean), 2):
            
            p1 = ord(text_clean[i]) - 65
            p2 = ord(text_clean[i+1]) - 65
            
         
            c1 = (matrix[0][0] * p1 + matrix[0][1] * p2) % 26
            c2 = (matrix[1][0] * p1 + matrix[1][1] * p2) % 26
            
            result += chr(c1 + 65) + chr(c2 + 65)
            
        return result

    def encrypt(self, text: str) -> str:
        if not text: return ""
        return self._process(text, self.matrix)

    def decrypt(self, text: str) -> str:
        if not text: return ""
      
        return self._process(text, self.inverse_matrix)