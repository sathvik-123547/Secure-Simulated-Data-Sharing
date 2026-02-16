# Security Protocol Specification

## 🛡️ Trust Model & Assumptions

The Security Architecture assumes a **Malicious Adversary** model for external actors and a **Semi-Honest (Honest-but-Curious)** model for the Cloud Service Provider.

| Entity | Trust Assumption | Capabilities |
| :--- | :--- | :--- |
| **Terminal** | Trusted | Can sign/encrypt data correctly. Vulnerable to physical capture. |
| **Edge Server**| **Root of Trust** | Holds Master Keys. Must be deployed in a TEE (Trusted Execution Environment) in production. |
| **Cloud** | Untrusted | trusted for availability, untrusted for confidentiality/integrity. |
| **TPA** | Trusted | Trusted to verify proofs correctly, but should not see data. |

## 🔐 Cryptographic Primitives

### 1. Fine-Grained Access Control: CP-ABE
We employ **Ciphertext-Policy Attribute-Based Encryption (CP-ABE)** to mathematically enforce access control.
-   **Scheme**: Bethencourt et al. (or Watered-Dual System standard).
-   **Logic**: Ciphertexts are associated with an Access Tree $\mathcal{T}$.
-   **Key Gen**: $SK = Gen(MSK, S)$ where $S$ is the set of user attributes.
-   **Decryption**: Possible iff $S \models \mathcal{T}$.
-   **Security**: Choose-Plaintext Attack (CPA) secure under the Generic Group Model.

### 2. Integrity Auditing: Homomorphic Signatures
To enable public auditing without data retrieval (Blockless Verification), we utilize **RSA-based Homomorphic Hash Functions** or **BLS-based Aggregate Signatures**.

#### The Protocol
1.  **Block Generation**: Data file $F$ is split into blocks $\{m_1, ..., m_n\}$.
2.  **Tagging**: Edge computes $\sigma_i = (H(id) \cdot g^{m_i})^\alpha$ for each block.
3.  **Challenge**: TPA sends a vector $Q = \{(i, \nu_i)\}_{i \in I}$ where $\nu_i$ is a random coefficient.
4.  **Proof**: Cloud parses $Q$, computes $\mu = \sum_{i \in I} \nu_i m_i$ and $\sigma = \prod_{i \in I} \sigma_i^{\nu_i}$.
5.  **Verification**: TPA checks if $e(\sigma, g) \stackrel{?}{=} e(\prod (H(id)^\alpha)^{\nu_i} \cdot g^\mu, h)$.

### 3. Transport Security
-   **mTLS (Mutual TLS)**: All internal communication (Edge $\leftrightarrow$ Cloud) is secured via mTLS 1.3 to prevent Man-in-the-Middle attacks.

## 4. Attack Vector Analysis & Mitigations

| Attack Type | Vector | Mitigation Strategy |
| :--- | :--- | :--- |
| **Collusion Attack** | Two users combine attributes (e.g., "Student" + "Professor") to decrypt data requiring both. | **CP-ABE Collusion Compliance**: Keys are randomized with a unique polynomial scalar $r$, making logical combination of keys across different users mathematically impossible. |
| **Replay Attack** | Adversary intercepts a valid write request and re-sends it to corrupt state. | **Nonce & Timestamping**: All API requests include a monotonic counter and strict timestamp window (<5s). |
| **Cloud Insider** | Cloud admin tries to read stored data. | **Zero-Knowledge Storage**: Cloud only holds $Enc_{ABE}(Data)$. Without the Attribute Keys, brute force is infeasible ($2^{256}$ complexity). |
| **Lazy Auditor** | TPA returns "Valid" without checking to save compute. | **Spot Checking**: The system occasionally injects invalid blocks; if TPA fails to flag them, its trust score is slashed (Game Theoretic security). |

## 🔑 Key Management
-   **Master Secret Key (MSK)**: Stored in an HSM (Hardware Security Module) simulated via secure vault.
-   **Attribute Keys**: Issued out-of-band to users after identity verification.
-   **Key Rotation**: Supports epoch-based key rotation to handle attribute revocation.
