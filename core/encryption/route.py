import math

class RouteCipher:
    def __init__(self, cols: int = 4):
       
        self.cols = max(2, int(cols))

    def encrypt(self, text: str) -> str:
        if not text: return ""
      
        length = len(text)
        rows = math.ceil(length / self.cols)
        
       
        total_chars = rows * self.cols
        padded_text = text.ljust(total_chars, 'X')
        
       
        grid = []
        for i in range(rows):
            grid.append(list(padded_text[i * self.cols : (i + 1) * self.cols]))
            
       
        result = []
        top, bottom = 0, rows - 1
        left, right = 0, self.cols - 1
        
    
        while top <= bottom and left <= right:
            # Üst satırı soldan sağa oku
            for i in range(left, right + 1):
                result.append(grid[top][i])
            top += 1
            
            # Sağ sütunu yukarıdan aşağı oku
            for i in range(top, bottom + 1):
                result.append(grid[i][right])
            right -= 1
            
            # Alt satırı sağdan sola oku
            if top <= bottom:
                for i in range(right, left - 1, -1):
                    result.append(grid[bottom][i])
                bottom -= 1
                
            # Sol sütunu aşağıdan yukarı oku
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    result.append(grid[i][left])
                left += 1
                
        return "".join(result)

    def decrypt(self, text: str) -> str:
        if not text: return ""
        
      
        length = len(text)
        rows = math.ceil(length / self.cols)
        
    
        grid = [['' for _ in range(self.cols)] for _ in range(rows)]
        
       
        index = 0
        top, bottom = 0, rows - 1
        left, right = 0, self.cols - 1
        
        while top <= bottom and left <= right:
            
            for i in range(left, right + 1):
                grid[top][i] = text[index]
                index += 1
            top += 1
            
            
            for i in range(top, bottom + 1):
                grid[i][right] = text[index]
                index += 1
            right -= 1
            
            
            if top <= bottom:
                for i in range(right, left - 1, -1):
                    grid[bottom][i] = text[index]
                    index += 1
                bottom -= 1
            
            
            if left <= right:
                for i in range(bottom, top - 1, -1):
                    grid[i][left] = text[index]
                    index += 1
                left += 1
                
      
        plain_text = ""
        for row in grid:
            plain_text += "".join(row)
            
      
        return plain_text.rstrip('X')