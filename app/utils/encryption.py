from cryptography.fernet import Fernet
from app.core.config import ENCRYPTION_KEY

# Fernet uses AES-128 internally but is industry-accepted secure encryption
cipher = Fernet(ENCRYPTION_KEY.encode())

def encrypt_text(plain_text: str) -> str:
    return cipher.encrypt(plain_text.encode()).decode()

def decrypt_text(cipher_text: str) -> str:
    return cipher.decrypt(cipher_text.encode()).decode()
