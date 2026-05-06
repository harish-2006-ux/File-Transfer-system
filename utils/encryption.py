"""
File Encryption/Decryption Utilities
Uses AES-256 Fernet encryption
"""

from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()

# Use environment key or generate fallback for deployment
encryption_key = os.getenv('ENCRYPTION_KEY')
if not encryption_key:
    # Generate key for deployment if not set
    key = Fernet.generate_key()
    print(f'⚠️  Generated encryption key: {key.decode()}')
    print('   Add to .env: ENCRYPTION_KEY=' + key.decode())
    KEY = key
else:
    KEY = encryption_key.encode()

cipher_suite = Fernet(KEY)


def encrypt_file(input_path: str, output_path: str) -> bool:
    """
    Encrypt a file using AES-256 Fernet
    
    Args:
        input_path: Path to file to encrypt
        output_path: Path to save encrypted file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        
        encrypted = cipher_suite.encrypt(data)
        
        with open(output_path, 'wb') as f:
            f.write(encrypted)
        
        return True
    except Exception as e:
        print(f"Encryption error: {e}")
        return False


def decrypt_file(input_path: str, output_path: str) -> bool:
    """
    Decrypt a file using AES-256 Fernet
    
    Args:
        input_path: Path to encrypted file
        output_path: Path to save decrypted file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        
        decrypted = cipher_suite.decrypt(data)
        
        with open(output_path, 'wb') as f:
            f.write(decrypted)
        
        return True
    except Exception as e:
        print(f"Decryption error: {e}")
        return False


def get_key() -> bytes:
    """Get the encryption key"""
    return KEY


if __name__ == '__main__':
    print('Encryption key:', get_key().decode())
