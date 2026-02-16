from cryptography.fernet import Fernet
import hashlib
import json
import os

class CryptoUtils:
    @staticmethod
    def generate_aes_key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt_aes(data: str, key: bytes) -> bytes:
        f = Fernet(key)
        return f.encrypt(data.encode())

    @staticmethod
    def decrypt_aes(ciphertext: bytes, key: bytes) -> str:
        f = Fernet(key)
        return f.decrypt(ciphertext).decode()

    @staticmethod
    def generate_mock_homomorphic_signature(data: str) -> int:
        """
        Simulates a homomorphic signature by hashing the data and mapping it to a finite field.
        In production, this would use RSA-based or BLS-based aggregation schemes.
        """
        h = hashlib.sha256(data.encode()).hexdigest()
        return int(h, 16) % 1000003  # large prime simulation
