import math

class ColumnarCipher:
    def __init__(self, key: str = "KEY"):
      
        self.key = key if key else "KEY"

    def _get_column_order(self):
   
        key_indexed = [(char, i) for i, char in enumerate(self.key)]
        key_indexed.sort() 
        return [item[1] for item in key_indexed]

    def encrypt(self, text: str) -> str:
        if not text: return ""
        
        order = self._get_column_order()
        num_cols = len(self.key)
        num_rows = math.ceil(len(text) / num_cols)
        

        padded_text = text.ljust(num_rows * num_cols, '_') # 
        
        
        grid = []
        for i in range(num_rows):
            grid.append(padded_text[i * num_cols : (i + 1) * num_cols])
            
      
        cipher_text = ""
        for col_idx in order:
            for row in grid:
                cipher_text += row[col_idx]
                
        return cipher_text

    def decrypt(self, text: str) -> str:
        if not text: return ""
        
        order = self._get_column_order()
        num_cols = len(self.key)
        num_rows = math.ceil(len(text) / num_cols)
        
     
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        
        idx = 0
        for col_idx in order:
            for row_idx in range(num_rows):
                if idx < len(text):
                    grid[row_idx][col_idx] = text[idx]
                    idx += 1
                    
       
        plain_text = ""
        for row in grid:
            plain_text += "".join(row)
            
        
        return plain_text.rstrip('_')