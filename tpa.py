import json
import hashlib
import os

CLOUD_DB_PATH = "data/cloud_registry.json"

# Recalculate homomorphic signature (simulated)
def generate_signature(data: bytes):
    h = hashlib.sha256(data).hexdigest()
    return int(h, 16) % 1000003

# Load data block from cloud
def get_cloud_block(block_id):
    if not os.path.exists(CLOUD_DB_PATH):
        print("[TPA] Error: Cloud registry not found.")
        return None
    with open(CLOUD_DB_PATH, 'r') as f:
        cloud_data = json.load(f)
    return cloud_data.get(block_id, None)

# Verify block integrity
def audit_block(block_id):
    block = get_cloud_block(block_id)
    if not block:
        print(f"[TPA] Block {block_id} not found.")
        return

    data = block["data"]
    stored_signature = block["signature"]
    recalculated_signature = generate_signature(data.encode())

    print(f"[TPA] Stored Signature:     {stored_signature}")
    print(f"[TPA] Recalculated Signature: {recalculated_signature}")

    if int(stored_signature) == recalculated_signature:
        print(f"[TPA] ✅ Integrity Verified for {block_id}")
    else:
        print(f"[TPA] ❌ Integrity Check Failed for {block_id}")

# Main
if __name__ == "__main__":
    block_id = input("Enter block ID to audit: ")
    audit_block(block_id)
