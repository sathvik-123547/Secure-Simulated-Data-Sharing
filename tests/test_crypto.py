import pytest
from src.common.bls_engine import BLSEngine
from src.common.abe_engine import KPABEEngine

def test_bls_signature():
    print("\n--- Testing BLS Engine ---")
    sk, pk = BLSEngine.keygen()
    message = "audit-me-please"
    
    # 1. Sign
    sigma = BLSEngine.sign(sk, message)
    
    # 2. Verify
    assert BLSEngine.verify(pk, message, sigma)
    print("✅ BLS Sign/Verify passed")
    
    # 3. Aggregate
    msg2 = "second-block"
    sigma2 = BLSEngine.sign(sk, msg2)
    agg = BLSEngine.aggregate_signatures([sigma, sigma2])
    
    # 4. Batch Verify (Same PK, diff messages)
    # verify_batch logic check
    assert BLSEngine.verify_batch(pk, [message, msg2], agg)
    print("✅ BLS Aggregation passed")

def test_kp_abe():
    print("\n--- Testing KP-ABE Engine ---")
    pk, mk = KPABEEngine.setup()
    
    # 1. KeyGen for "researcher"
    sk_res = KPABEEngine.keygen(mk, "researcher")
    
    # 2. Encrypt for "researcher"
    # Note: Our simple KP-ABE encrypts a Key.
    # We simulate message encryption by just checking Key Recovery.
    attrs = ["researcher", "A"]
    ct = KPABEEngine.encrypt(pk, 12345, attrs)
    
    # 3. Decrypt
    key_prime = KPABEEngine.decrypt(ct, sk_res)
    
    # Verify the encapsulated key key_prime matches what's in CT
    # In KEM, Decrypt returns the shared secret.
    # The 's' was random, so we can't check against a known input M directly 
    # unless we return K from Encrypt too (standard KEM API).
    # *Correction*: My KPABEEngine.encrypt returns E_prime which IS the encapsulated key check value?
    # No, E_prime IS the encapsulated key K.
    # Decrypt returns K.
    # So we check if Decrypt(CT) == CT['E_prime']
    # Wait, Decrypt logic:
    # recovered = pairing(d, E_i)
    # E_prime = pairing(y, g2)^s
    # They should be equal.
    
    assert key_prime == ct['E_prime']
    print("✅ KP-ABE Decrypt passed")
    
    # 4. Fail Case
    sk_doc = KPABEEngine.keygen(mk, "doctor")
    try:
        KPABEEngine.decrypt(ct, sk_doc)
        assert False, "Should have failed"
    except ValueError:
        print("✅ KP-ABE Access Denied passed")
