from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Generate valid key if not set
if 'ENCRYPTION_KEY' not in os.environ or not os.getenv('ENCRYPTION_KEY'):
    key = Fernet.generate_key()
    print(f'Generated new encryption key: {key.decode()}')
    print('Add to .env: ENCRYPTION_KEY=' + key.decode())
    KEY = key
else:
    KEY = os.getenv('ENCRYPTION_KEY').encode()

cipher_suite = Fernet(KEY)

async def encrypt_file(input_path: str, output_path: str):
    """Async file encryption."""
    loop = asyncio.get_event_loop()
    with open(input_path, 'rb') as f:
        data = await loop.run_in_executor(None, f.read)
    encrypted = cipher_suite.encrypt(data)
    with open(output_path, 'wb') as f:
        f.write(encrypted)

async def decrypt_file(input_path: str, output_path: str):
    """Async file decryption."""
    loop = asyncio.get_event_loop()
    with open(input_path, 'rb') as f:
        data = await loop.run_in_executor(None, f.read)
    decrypted = cipher_suite.decrypt(data)
    with open(output_path, 'wb') as f:
        f.write(decrypted)

def get_key() -> bytes:
    return KEY

if __name__ == '__main__':
    print('New encryption key:', get_key().decode())
