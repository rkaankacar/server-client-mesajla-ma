class Rot13Cipher:
    def __init__(self):
        
        pass

    def _transform(self, text: str) -> str:
        result = ""
        for char in text:
            if 'a' <= char <= 'z':
                
                result += chr(((ord(char) - ord('a') + 13) % 26) + ord('a'))
            elif 'A' <= char <= 'Z':
                
                result += chr(((ord(char) - ord('A') + 13) % 26) + ord('A'))
            else:
                
                result += char
        return result

    def encrypt(self, text: str) -> str:
        return self._transform(text)

    def decrypt(self, text: str) -> str:
       
        return self._transform(text)