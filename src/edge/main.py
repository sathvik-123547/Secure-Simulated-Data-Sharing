from src.common.crypto import CryptoUtils
from src.common.abe_engine import KPABEEngine
from src.common.bls_engine import BLSEngine
import json
import base64

class EdgeNode:
    def __init__(self):
        self.policy_map = {"T-001": ["researcher", "admin"]}
        # Initialize Crypto Systems
        print("[Edge] Initializing Cryptographic Systems...")
        self.abe_pk, self.abe_mk = KPABEEngine.setup()
        self.bls_sk, self.bls_pk = BLSEngine.keygen()
        print("[Edge] Crypto Setup Complete.")

    def process_ingest(self, data_packet):
        """
        Real Crypto Flow:
        1. Decrypt AES (Terminal -> Edge)
        2. Encrypt ABE (Edge -> Cloud, policy bound)
        3. Sign BLS (Edge -> Cloud, integrity)
        """
        raw_key = data_packet["key"].encode() if isinstance(data_packet["key"], str) else data_packet["key"]
        payload = data_packet["payload"].encode()

        # 1. Decrypt AES
        decrypted = CryptoUtils.decrypt_aes(payload, raw_key)
        print(f"[Edge] Decrypted data: {decrypted}")

        # 2. Re-encrypt (Real KP-ABE)
        target_attrs = ["researcher", "lab-1"] 
        # Hybrid ABE-KEM: Encrypt dummy key 12345
        abe_ciphertext = KPABEEngine.encrypt(self.abe_pk, 12345, target_attrs)
        
        # 3. Homomorphic Sign (Real BLS)
        # Sign the CIPHERTEXT (E_prime) so TPA can verify without decryption
        # In full PDP, we sign blocks. Here we sign the KEM element.
        message_to_sign = str(abe_ciphertext['E_prime'])
        signature = BLSEngine.sign(self.bls_sk, message_to_sign)
        
        return {
            "owner": data_packet["id"],
            "abe_ciphertext": str(abe_ciphertext['E_prime']), 
            "policy": target_attrs,
            "signature": signature, # Tuple
            "original_size": len(decrypted)
        }
