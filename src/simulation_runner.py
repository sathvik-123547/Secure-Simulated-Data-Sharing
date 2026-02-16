from src.terminal.main import TerminalAgent
from src.edge.main import EdgeNode
from src.cloud.main import CloudRegistry
from src.tpa.main import ThirdPartyAuditor # Corrected import path
import time

def run_simulation():
    print("=== Starting Secure Data Sharing Simulation (Enterprise Mode) ===\n")

    # 1. Initialize Components
    terminal = TerminalAgent("T-001")
    edge = EdgeNode()
    cloud = CloudRegistry()
    tpa = ThirdPartyAuditor()

    # 2. Terminal generates and sends data
    print("--- Phase 1: Ingestion ---")
    data_packet = terminal.send_data()
    # In a real API, this would be a POST request
    
    # 3. Edge processes data
    print("\n--- Phase 2: Edge Processing (Re-Encryption & Signing) ---")
    processed_data = edge.process_ingest(data_packet)
    
    # 4. Cloud stores data
    print("\n--- Phase 3: Cloud Storage ---")
    block_id = f"block-{int(time.time())}"
    cloud.store(block_id, processed_data)

    # 5. TPA Audits data
    print("\n--- Phase 4: Integrity Audit ---")
    # Verify using the Real BLS Key from Edge (Simulating Public Key retrieval)
    # in real world, TPA gets PK from PKI.
    tpa.challenge_cloud_real(cloud, block_id, edge.bls_pk)

    print("\n=== Simulation Complete ===")

if __name__ == "__main__":
    run_simulation()
