class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt(self, text, key):
        # Create empty columns
        columns = [''] * key
        
        # Fill columns
        for i, char in enumerate(text):
            columns[i % key] += char
            
        # Join columns
        return ''.join(columns)

    def decrypt(self, text, key):
        # Calculate number of rows
        rows = len(text) // key
        remaining = len(text) % key
        
        # Calculate characters per column
        chars_per_col = [rows + 1 if i < remaining else rows for i in range(key)]
        
        # Create empty result
        result = [''] * len(text)
        
        # Calculate start positions for each column
        start_pos = 0
        for i in range(key):
            # Fill this column
            for j in range(chars_per_col[i]):
                if start_pos + j < len(text):
                    result[i + j * key] = text[start_pos + j]
            start_pos += chars_per_col[i]
            
        return ''.join(result)

def transposition_encrypt(text: str, key: int) -> str:
    """
    Encrypt text using Transposition cipher.
    
    Args:
        text (str): Text to encrypt
        key (int): Number of columns
        
    Returns:
        str: Encrypted text
    """
    cipher = TranspositionCipher()
    return cipher.encrypt(text, key)

def transposition_decrypt(text: str, key: int) -> str:
    """
    Decrypt text using Transposition cipher.
    
    Args:
        text (str): Text to decrypt
        key (int): Number of columns
        
    Returns:
        str: Decrypted text
    """
    cipher = TranspositionCipher()
    return cipher.decrypt(text, key)