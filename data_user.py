import json
import os
from cryptography.fernet import Fernet

# Simulated CP-ABE policy and user attributes
POLICY = ["researcher", "iot", "level1"]
user_attributes = ["iot", "researcher", "level1"]  # you can change to test denial

# File paths
KEY_PATH = "data/terminal_key.key"
ENCRYPTED_DIR = "data/encrypted"
CLOUD_DB_PATH = "data/cloud_registry.json"

# Check if user attributes satisfy policy
def access_granted(user_attrs, policy_attrs):
    return all(attr in user_attrs for attr in policy_attrs)

# Load AES key
def load_aes_key():
    with open(KEY_PATH, 'rb') as f:
        return f.read()

# Load encrypted ciphertext
def load_encrypted_data(block_id):
    path = os.path.join(ENCRYPTED_DIR, f"{block_id}.json")
    if not os.path.exists(path):
        print(f"[DU] Encrypted file {block_id} not found.")
        return None
    with open(path, 'r') as f:
        return json.load(f)["encrypted_data"]

# Decrypt using AES
def decrypt_data(ciphertext, key):
    f = Fernet(key)
    return f.decrypt(ciphertext.encode()).decode()

# Main logic
if __name__ == "__main__":
    block_id = input("Enter block ID to request: ")

    if access_granted(user_attributes, POLICY):
        print(f"[DU] ✅ Access granted based on attributes: {user_attributes}")
        
        enc_data = load_encrypted_data(block_id)
        if enc_data is None:
            exit()
        
        key = load_aes_key()
        plaintext = decrypt_data(enc_data, key)
        print(f"[DU] 🔓 Decrypted Data: {plaintext}")
    else:
        print(f"[DU] ❌ Access denied. Attributes do not satisfy policy.")
