import os
import json
from cryptography.fernet import Fernet
from datetime import datetime

# Paths
ENCRYPTED_DATA_DIR = "data/encrypted"
KEY_STORAGE_PATH = "data/terminal_key.key"

# Step 1: Generate AES Key
def generate_aes_key():
    key = Fernet.generate_key()
    with open(KEY_STORAGE_PATH, 'wb') as f:
        f.write(key)
    return key

# Step 2: Encrypt Data
def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data.encode())

# Step 3: Save Encrypted Data
def save_encrypted_data(ciphertext):
    if not os.path.exists(ENCRYPTED_DATA_DIR):
        os.makedirs(ENCRYPTED_DATA_DIR)
    filename = datetime.now().strftime("block_%Y%m%d_%H%M%S.json")
    path = os.path.join(ENCRYPTED_DATA_DIR, filename)
    with open(path, 'w') as f:
        json.dump({"encrypted_data": ciphertext.decode()}, f)
    print(f"Encrypted data saved to {path}")

# Step 4: Mock Data Generator
def generate_mock_data():
    import random
    temp = round(random.uniform(24.0, 30.0), 2)
    log = f"Temperature reading: {temp}°C"
    return log

# Main Flow
if __name__ == "__main__":
    data = generate_mock_data()
    print(f"[Terminal] Generated Data: {data}")

    aes_key = generate_aes_key()
    ciphertext = encrypt_data(data, aes_key)

    save_encrypted_data(ciphertext)

