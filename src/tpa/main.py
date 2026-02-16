from src.common.bls_engine import BLSEngine

class ThirdPartyAuditor:
    def __init__(self):
        pass

    def challenge_cloud(self, cloud_registry, block_id):
        pass # Deprecated

    def challenge_cloud_real(self, cloud_registry, block_id, schema_pk):
        print(f"[TPA] Challenging Cloud for Block {block_id}...")
        
        # 1. Get Data Metadata from Cloud
        data_block = cloud_registry.retrieve(block_id)
        if not data_block:
             print("[TPA] Block not found!")
             return

        # 2. Extract Data
        stored_signature = data_block["signature"]
        stored_cipher = data_block["abe_ciphertext"]
        
        print(f"[TPA] Verifying Signature on stored ciphertext...")
        
        # 3. Verify BLS Signature
        # e(sigma, g2) == e(H(m), pk)
        is_valid = BLSEngine.verify(schema_pk, stored_cipher, stored_signature)
        
        if is_valid:
             print(f"[TPA] ✅ Integrity Verified for {block_id} (BLS Signature Match)")
             return True
        else:
             print(f"[TPA] ❌ Integrity Check Failed!")
             return False
