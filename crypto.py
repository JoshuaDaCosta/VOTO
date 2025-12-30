from cryptography.fernet import Fernet
from hashlib import sha256
import os 
# ⚠️ CHAVE GERADA UMA ÚNICA VEZ
CHAVE =b'pLwo65-UfpNNuCJH0zOaCC1EjU9kh6uYpbtInYMskPE='

cipher = Fernet(CHAVE)


def encrypt_user(valor: str) -> str:
    return cipher.encrypt(valor.encode()).decode()


def decrypt_user(valor: str) -> str:
    return cipher.decrypt(valor.encode()).decode()

def hash_user(valor: str) -> str:
    import hashlib
    return hashlib.sha256((valor).encode()).hexdigest()


