class DESCipher:
    def __init__(self, key: str = "KEY"):
       
        self.key_bin = self._text_to_bin(key)
        if len(self.key_bin) < 8:
            self.key_bin = self.key_bin.ljust(8, '0')

    def _text_to_bin(self, text):
        return ''.join(format(ord(c), '08b') for c in text)

    def _bin_to_text(self, binary):
        text = ""
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            text += chr(int(byte, 2))
        return text

    def _xor(self, a, b):
        
        res = ""
        for i in range(len(a)):
            if a[i] == b[i]: res += "0"
            else: res += "1"
        return res

    def _feistel_function(self, right_block, subkey):
       
        if len(subkey) > len(right_block):
            subkey = subkey[:len(right_block)]
        elif len(subkey) < len(right_block):
            subkey = subkey.ljust(len(right_block), '0')
        
        return self._xor(right_block, subkey)

    def _process_block(self, block, mode):
       
        n = len(block)
        mid = n // 2
        left = block[:mid]
        right = block[mid:]
        
      
        keys = [self.key_bin, self.key_bin[::-1]]
        
        if mode == "decrypt":
            keys = keys[::-1] 
            
        for k in keys:
            temp = right
      
            func_res = self._feistel_function(right, k)
            right = self._xor(left, func_res)
            left = temp
            
        return left + right 

    def encrypt(self, text: str) -> str:
        if not text: return ""
        binary_text = self._text_to_bin(text)
        
        res_bin = ""
       
        for i in range(0, len(binary_text), 8):
            block = binary_text[i:i+8]
            res_bin += self._process_block(block, "encrypt")
            
    
        hex_res = ""
        for i in range(0, len(res_bin), 4):
            chunk = res_bin[i:i+4]
            hex_res += hex(int(chunk, 2))[2:].upper()
        return hex_res

    def decrypt(self, text: str) -> str:
        if not text: return ""
        try:
            
            binary_text = ""
            for c in text:
                binary_text += format(int(c, 16), '04b')
            
            res_bin = ""
            for i in range(0, len(binary_text), 8):
                block = binary_text[i:i+8]
                res_bin += self._process_block(block, "decrypt")
                
            return self._bin_to_text(res_bin)
        except:
            return "DES Hatası"