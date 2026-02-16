import requests
import time
from src.common.crypto import CryptoUtils

EDGE_URL = "http://127.0.0.1:8000"
CLOUD_URL = "http://127.0.0.1:8001"

def inject():
    print("--- Injecting Mock Telemetry Data ---")
    
    # 1. Generate Data
    key = CryptoUtils.generate_aes_key()
    data = "Critical-Infrastructure-Status: OK"
    enc_data = CryptoUtils.encrypt_aes(data, key)
    
    payload = {
        "id": "T-001",
        "payload": enc_data.decode(),
        "key": key.decode()
    }
    
    # 2. Send to Edge
    print(f"[Terminal] Sending to {EDGE_URL}/ingest...")
    try:
        r = requests.post(f"{EDGE_URL}/ingest", json=payload)
        if r.status_code != 200:
            print(f"❌ Edge Ingest Failed: {r.text}")
            return
            
        processed_data = r.json()["processed_data"]
        print("✅ Edge Processed Data (Re-encrypted & Signed)")
        
        # 3. Store in Cloud (Simulating Edge->Cloud push)
        # In a real app, Edge would do this async. Here we do it manually for the demo flow control.
        # Wait, the EdgeNode.process_ingest returns dict. The API src/edge/api.py returns it.
        # But src/edge/api.py DOES NOT push to cloud automatically in the current implementation?
        # Let's check src/edge/api.py.
        # It just returns {"status": "success", "processed_data": processed}.
        # So we (the script) act as the network transport to Cloud.
        
        store_payload = {
            "block_id": "block-test-api",
            "data_object": processed_data
        }
        
        print(f"[Edge->Cloud] Pushing to {CLOUD_URL}/store...")
        r2 = requests.post(f"{CLOUD_URL}/store", json=store_payload)
        
        if r2.status_code == 200:
            print(f"✅ Data Stored successfully as 'block-test-api'")
            print("👉 You can now check the Dashboard!")
        else:
             print(f"❌ Cloud Store Failed: {r2.text}")
             
    except Exception as e:
        print(f"❌ Injection Failed: {str(e)}")

if __name__ == "__main__":
    inject()
