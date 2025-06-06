import os
import json

SIGNED_DIR = "data/signed"
CLOUD_DB_PATH = "data/cloud_registry.json"

# Step 1: Upload signed data to cloud (register it)
def upload_to_cloud():
    registry = {}
    for file in os.listdir(SIGNED_DIR):
        if file.endswith(".json"):
            file_path = os.path.join(SIGNED_DIR, file)
            with open(file_path, 'r') as f:
                content = json.load(f)
            block_id = file.replace(".json", "")
            registry[block_id] = {
                "data": content["data"],
                "signature": content["signature"]
            }

    with open(CLOUD_DB_PATH, 'w') as f:
        json.dump(registry, f, indent=4)
    print(f"[Cloud Server] Uploaded {len(registry)} blocks to simulated cloud.")

# Step 2: Return data block (for DU or TPA)
def fetch_data_block(block_id):
    if not os.path.exists(CLOUD_DB_PATH):
        print("No cloud data found.")
        return None
    with open(CLOUD_DB_PATH, 'r') as f:
        cloud_data = json.load(f)
    return cloud_data.get(block_id, None)

# Main
if __name__ == "__main__":
    upload_to_cloud()

    # Simulate a fetch test
    test_id = input("Enter block ID to fetch (for test): ")
    result = fetch_data_block(test_id)
    if result:
        print(f"[Cloud Server] Block Found: {result}")
    else:
        print("[Cloud Server] Block not found.")
