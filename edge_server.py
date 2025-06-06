import json
import os
import hashlib
from cryptography.fernet import Fernet

ENCRYPTED_DIR = "data/encrypted"
SIGNED_DIR = "data/signed"
KEY_PATH = "data/terminal_key.key"

# Simulated policy
POLICY = ["researcher", "iot", "level1"]

# Simulate user attribute check (CP-ABE)
def cp_abe_policy_check(user_attrs, policy_attrs):
    return all(attr in user_attrs for attr in policy_attrs)

# Simulated homomorphic signature (hash mod prime)
def generate_signature(data: bytes):
    h = hashlib.sha256(data).hexdigest()
    return int(h, 16) % 1000003  # using a large prime

# Decrypt data using AES key
def decrypt_data(ciphertext: str, key: bytes):
    f = Fernet(key)
    return f.decrypt(ciphertext.encode()).decode()

# Save signed data
def save_signed_data(data_id, data, signature):
    if not os.path.exists(SIGNED_DIR):
        os.makedirs(SIGNED_DIR)
    path = os.path.join(SIGNED_DIR, f"{data_id}.json")
    with open(path, 'w') as f:
        json.dump({"data": data, "signature": signature}, f)
    print(f"[Edge Server] Signed data saved to {path}")

# Main Flow
if __name__ == "__main__":
    user_attributes = ["iot", "researcher", "level1"]  # Simulated DU attributes

    for file in os.listdir(ENCRYPTED_DIR):
        if file.endswith(".json"):
            with open(os.path.join(ENCRYPTED_DIR, file), 'r') as f:
                enc_content = json.load(f)

            with open(KEY_PATH, 'rb') as f:
                key = f.read()

            encrypted_data = enc_content["encrypted_data"]

            # Simulate access control
            if cp_abe_policy_check(user_attributes, POLICY):
                print(f"[Edge Server] Access granted for file {file}")
                decrypted_data = decrypt_data(encrypted_data, key)
                signature = generate_signature(decrypted_data.encode())
                data_id = file.split(".")[0]
                save_signed_data(data_id, decrypted_data, signature)
            else:
                print(f"[Edge Server] Access denied for file {file}")
