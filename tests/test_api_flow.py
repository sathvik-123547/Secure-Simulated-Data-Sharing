import requests
import time
import json

EDGE_URL = "http://127.0.0.1:8000"
CLOUD_URL = "http://127.0.0.1:8001"

def test_system_flow():
    print("=== Testing Microservices Flow ===")
    
    # Wait for services
    time.sleep(2)
    
    # 1. Health Check
    try:
        r = requests.get(f"{EDGE_URL}/health")
        print(f"[Edge] Health: {r.json()}")
    except Exception as e:
        print(f"[Edge] Failed: {e}")
        return

    # 2. Ingest
    payload = {
        "id": "T-001",
        "payload": "mock-encrypted-aes-data", # Edge expects string for now, will decode/decrypt it. 
        # Wait, Edge process_ingest expects REAL AES encrypted payload.
        # We need to use CryptoUtils to encrypt first.
        "key": "mock-key"
    }
    
    # Let's import CryptoUtils to make a valid packet
    from src.common.crypto import CryptoUtils
    key = CryptoUtils.generate_aes_key()
    data = "High-Security-Telemetry"
    enc_data = CryptoUtils.encrypt_aes(data, key)
    
    payload = {
        "id": "T-001",
        "payload": enc_data.decode(),
        "key": key.decode()
    }
    
    print("\n[Terminal] Sending Data to Edge...")
    r = requests.post(f"{EDGE_URL}/ingest", json=payload)
    if r.status_code == 200:
        resp = r.json()
        print(f"[Edge] Response: {resp}")
        processed = resp["processed_data"]
        
        # 3. Store in Cloud
        print("\n[Edge->Cloud] Storing Data...")
        store_payload = {
            "block_id": "block-test-api",
            "data_object": processed
        }
        r2 = requests.post(f"{CLOUD_URL}/store", json=store_payload)
        print(f"[Cloud] Store Response: {r2.json()}")
        
        # 4. Verify Retrieval
        print("\n[TPA->Cloud] Retrieving Block...")
        r3 = requests.get(f"{CLOUD_URL}/block/block-test-api")
        print(f"[Cloud] Retrieved: {r3.json()}")
    else:
        print(f"[Edge] Error {r.status_code}: {r.text}")

if __name__ == "__main__":
    test_system_flow()
