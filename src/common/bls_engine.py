from py_ecc.bn128 import G1, G2, pairing, multiply, add, curve_order, Z1, Z2
from py_ecc.bn128 import final_exponentiate
import hashlib
from typing import Tuple, List

class BLSEngine:
    """
    Implements BLS Signature Scheme for Homomorphic Integrity Auditing.
    Uses BN128 curve.
    
    Properties:
    - KeyGen: SK, PK
    - Sign: sigma = H(m)^SK
    - Verify: e(sigma, g2) == e(H(m), PK)
    - Aggregate: sigma_agg = prod(sigma_i)
    """

    @staticmethod
    def keyinfo():
        return {"curve": "bn128", "order": curve_order}

    @staticmethod
    def keygen() -> Tuple[int, Tuple]:
        """Generates (SecretKey, PublicKey)"""
        # SK is a random integer < curve_order
        import secrets
        sk = secrets.randbelow(curve_order)
        # PK = g2^sk
        pk = multiply(G2, sk)
        return sk, pk

    @staticmethod
    def hash_to_point(message: str):
        """Hashes a message to a point on G1."""
        # Simple hash-to-curve (NOT secure for production, fine for demo)
        # In prod: use proper MapToG1 algorithm
        h = hashlib.sha256(message.encode()).digest()
        val = int.from_bytes(h, 'big') % curve_order
        return multiply(G1, val)

    @staticmethod
    def sign(sk: int, message: str):
        """sigma = H(m)^sk"""
        h_point = BLSEngine.hash_to_point(message)
        sigma = multiply(h_point, sk)
        return sigma

    @staticmethod
    def verify(pk: Tuple, message: str, sigma: Tuple) -> bool:
        """
        Check e(sigma, G2) == e(H(m), PK)
        Optimization: e(sigma, G2) * e(H(m), -PK) == 1
        """
        h_point = BLSEngine.hash_to_point(message)
        
        # LHS = pairing(G2, sigma)  # py_ecc pairing takes (G2, G1)
        lhs = pairing(G2, sigma)
        
        # RHS = pairing(PK, H(m))
        rhs = pairing(pk, h_point)
        
        return lhs == rhs

    @staticmethod
    def aggregate_signatures(signatures: List[Tuple]):
        """sigma_agg = sum(sigma_i) (Elliptic Curve Addition)"""
        if not signatures:
            return Z1
        agg = signatures[0]
        for sig in signatures[1:]:
            agg = add(agg, sig)
        return agg

    @staticmethod
    def verify_batch(pk: Tuple, messages: List[str], sigma_agg: Tuple) -> bool:
        """
        Verify aggregate signature:
        e(sigma_agg, G2) == prod( e(H(m_i), PK) )
        Note: This assumes all messages signed by SAME PK.
        """
        lhs = pairing(G2, sigma_agg)
        
        rhs = 1
        for msg in messages:
            h = BLSEngine.hash_to_point(msg)
            rhs = rhs * pairing(pk, h) # This works if pairing outputs FQ12 element supporting mult
            
        return lhs == rhs
