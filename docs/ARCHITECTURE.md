# High-Level System Architecture (v2.0)

## 🏗️ Architectural Philosophy
The **SecureData Layer** is built upon the principles of **Zero-Trust**, **Defense-in-Depth**, and **Verifiable Computing**. It adopts a distributed microservices architecture to ensure scalability, fault isolation, and independent deployability of critical components.

### Core Design Patterns
1.  **Microservices Architecture**: Each component (Terminal, Edge, Cloud) operates as a distinct service with defined boundaries and interfaces.
2.  **Event-Driven Communication**: Asynchronous data flow for high-throughput ingestion and processing.
3.  **Stateless Compute (Edge/Cloud)**: Services scale horizontally based on load, with state persisted only in dedicated data stores.

## 🧩 System Components

### 1. Terminal Layer (IoT Proving Ground)
*Role: Data Genesis & First-Mile Security*
-   **Function**: Simulates high-fidelity IoT agents (Smart Grids, Autonomous Vehicles, Medical Devices).
-   **Security**: Establishes a hardware-root-of-trust (simulated) to perform initial **AES-256-GCM** encryption.
-   **Protocol**: Pushes encrypted telemetry via lightweight Protocols (MQTT/CoAP or HTTP/2) to the Edge.

### 2. Edge Layer (The Trust Boundary)
*Role: Policy Enforcement & Cryptographic Transformation*
-   **Function**: Acts as the secure gateway between the insecure field (Terminals) and the semi-trusted Cloud.
-   **Key Operations**:
    -   **Proxy Re-Encryption**: Transforms symmetric ciphertexts into CP-ABE ciphertexts without exposing plaintext.
    -   **Homomorphic Tagging**: Computes integrity tags $\sigma$ on encrypted blocks to enable future auditing.
-   **Trust Level**: **High**. This layer manages the Attribute Authority (AA) and Master Secrets.

### 3. Cloud Storage Layer (The Vault)
*Role: Scalable, Oblivious Storage*
-   **Function**: Provides petabyte-scale storage for encrypted blobs and signature metadata.
-   **Characteristics**:
    -   **Oblivious**: The cloud provider cannot see the data (Encrypted) nor forge proofs (Unforgeable Signatures).
    -   **Verifiable**: Responds to probabilistic challenges from Auditors.

### 4. Third-Party Auditor (The Watchdog)
*Role: Independent Verification*
-   **Function**: Periodically challenges the Cloud Layer to prove data possession and integrity.
-   **Mechanism**: Uses **Homomorphic Signature Verification** ($Verify(\mu, \sigma)$) to detect bit-rot or malicious modification with >99.9% probability.

### 5. Frontend Dashboard (The Window)
*Role: Visualization & Control*
-   **Function**: Provides a real-time UI for auditors to inspect system health and verification status.
-   **Tech**: Vanilla JS (No-Build) / CSS3.
-   **Integration**: Polls TPA Service for audit results using `fetch`.

## 📐 Interaction Flow (Data Lifecycle)

### Stage 1: Secure Ingestion
> **Terminal** $\xrightarrow{AES}$ **Edge**
> Data is encrypted at source. The Edge receives opaque blobs, ensuring protection against network eavesdropping.

### Stage 2: Policy Binding
> **Edge** $\xrightarrow{CP-ABE}$ **Cloud**
> The Edge re-encrypts the data under a strict policy $P$ (e.g., `(Dept=HR AND Level>3)`). It also appends a Homomorphic Signature $\Phi$.

### Stage 3: Sovereign Access
> **User** $\xleftarrow{Decrypt}$ **Cloud**
> Authorized users download the ciphertext. Decryption is only possible if their local Secret Key $SK_{Attributes}$ satisfies Policy $P$.

## 🔮 Scalability Considerations
-   **Horizontal Scaling**: Edge nodes can be clustered behind a Load Balancer to handle millions of concurrent IoT streams.
-   **Database Sharding**: The Cloud registry leverages sharded databases (e.g., Cassandra/DynamoDB patterns) for metadata management.
