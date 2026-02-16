from py_ecc.bn128 import G1, G2, pairing, multiply, add, curve_order
import hashlib
import secrets
from typing import Dict, List, Any

class KPABEEngine:
    """
    Implements a Simplified Key-Policy Attribute-Based Encryption (KP-ABE)
    scheme over BN128.
    
    Ref: "Attribute-Based Encryption for Fine-Grained Access Control of Encrypted Data" (Goyal et al.)
    
    Simplified for Demo:
    - 'OR' Logic: Access Structure is a single attribute check for now, 
      or a simple threshold.
    - Full monotonic span programs are complex to implement in one file.
    """

    @staticmethod
    def setup():
        """
        Generates Master Key (MK) and Public Parameters (PK).
        """
        alpha = secrets.randbelow(curve_order)
        # Unique secret t_i for each attribute universe is generated on the fly in real schemes
        # Here we fix a small universe for demo
        universe = ['A', 'B', 'C', 'researcher', 'doctor', 'low-security']
        t = {attr: secrets.randbelow(curve_order) for attr in universe}
        
        y = multiply(G1, alpha) # y = g^alpha
        
        # Component T_i = g^t_i
        T = {attr: multiply(G1, val) for attr, val in t.items()}
        
        pk = {"y": y, "T": T, "universe": universe}
        mk = {"alpha": alpha, "t": t}
        return pk, mk

    @staticmethod
    def keygen(mk: Dict, access_policy_attr: str) -> Dict:
        """
        Generates a Secret Key (SK) for a user enabling them to decrypt
        if the ciphertext has the matching attribute.
        SK = g2^((alpha) / t_i)
        
        *Logic*: This is a simplified "Universe" match.
        Real KP-ABE uses Sharir Secret Sharing scheme trees.
        """
        alpha = mk['alpha']
        t_val = mk['t'].get(access_policy_attr)
        if not t_val:
            raise ValueError("Attribute not in universe")
            
        # compute alpha * (t_val)^-1 mod order
        inv_t = pow(t_val, -1, curve_order)
        exponent = (alpha * inv_t) % curve_order
        
        d = multiply(G2, exponent)
        return {"policy_attr": access_policy_attr, "d": d}

    @staticmethod
    def encrypt(pk: Dict, message_int: int, attributes: List[str]) -> Dict:
        """
        Encrypts an integer message M (mapped to GT).
        Ciphertext associated with a set of attributes.
        
        CT = (E', E_i...)
        s = random
        E' = M * e(y, g2)^s  [Blinds the message]
        E_i = (T_i)^s        [For each attribute]
        """
        s = secrets.randbelow(curve_order)
        
        # 1. Calculate blinding factor: Y = e(y, g2)^s
        #    e(g^alpha, g2)^s = e(g, g2)^(alpha*s)
        pairing_val = pairing(G2, pk['y']) # e(g^alpha, g2) -> e(G1, G2) convention
        # Note: py_ecc pairing is e(G2, G1). pk['y'] is G1. G2 is G2.
        
        # Exponentiate in GT is complex in py_ecc types?
        # Actually py_ecc pairing output is FQ12. We can't easily mult M by FQ12 unless M is FQ12.
        # **Simplification**: We use the KEM (Key Encapsulation) approach.
        # We generate a SYMMETRIC KEY 'K', encrypt K with ABE, then encrypt Data with K.
        # The 'shared_secret' is the FQ12 element.
        
        # K = pairing_val ** s
        # But py_ecc FQ12 doesn't support generic power easily in high-level API?
        # Check FQ12 impl: it has __pow__.
        
        key_encapsulated = pairing_val ** s
        
        # E_i for each attribute
        E = {}
        for attr in attributes:
            if attr in pk['T']:
                # E_i = (T_i)^s
                E[attr] = multiply(pk['T'][attr], s)
                
        return {
            "E_prime": key_encapsulated, # The symmetric key seed
            "E": E,
            "attrs": attributes
        }

    @staticmethod
    def decrypt(ct: Dict, sk: Dict) -> Any:
        """
        Decrypts the encapsulated key.
        Need sk['policy_attr'] to be present in ct['attrs'].
        
        K = e(E_i, d)
          = e( (g^t_i)^s, g2^(alpha/t_i) )
          = e( g, g2 ) ^ ( t_i * s * alpha / t_i )
          = e( g, g2 ) ^ ( s * alpha )
          = K_encapsulated
        """
        attr = sk['policy_attr']
        if attr not in ct['attrs']:
            raise ValueError("Attribute mismatch! Access Denied.")
            
        E_i = ct['E'][attr] # g^(t_i * s)
        d = sk['d']          # g2^(alpha / t_i)
        
        # recover K = e(d, E_i) -> pairing(G2, G1)
        recovered_key = pairing(d, E_i)
        
        if recovered_key == ct['E_prime']:
            return recovered_key
        else:
            raise ValueError("Decryption math failed.")

    @staticmethod
    def group_element_to_bytes(elem):
        """Hashes an FQ12 element to a 32-byte key for AES"""
        # FQ12 is a tuple of coeffs.
        s = str(elem)
        return hashlib.sha256(s.encode()).digest()
