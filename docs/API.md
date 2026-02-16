# API Specification (v2.0)

## 1. Edge Service
-   **Base URL**: `http://localhost:8000`

### `POST /ingest`
Receives encrypted telemetry from Terminal.
-   **Payload**:
    ```json
    {
      "id": "T-001",
      "payload": "<AES-Encrypted-Base64>",
      "key": "<AES-Key-Base64>"
    }
    ```
-   **Response**:
    ```json
    {
      "status": "success",
      "processed_data": {
        "owner": "T-001",
        "abe_ciphertext": "...",
        "signature": "..."
      }
    }
    ```

---

## 2. Cloud Service
-   **Base URL**: `http://localhost:8001`

### `POST /store`
Stores processed data blocks.
-   **Payload**:
    ```json
    {
      "block_id": "block-123",
      "data_object": { ... }
    }
    ```
-   **Response**: `{"status": "stored", "block_id": "block-123"}`

### `GET /block/{block_id}`
Retrieves data block for user access or auditing.
-   **Response**: Returns the JSON data object (Ciphertext + Signature).

---

## 3. TPA Service (Auditor)
-   **Base URL**: `http://localhost:8002`

### `POST /audit/{block_id}`
Triggers a real-time integrity verification.
-   **Process**:
    1.  Fetches `block_id` from Cloud Service.
    2.  Extracts BLS Signature and Ciphertext.
    3.  Performs Cryptographic Verification (`e(sig, g2) == e(H(m), pk)`).
-   **Response**:
    ```json
    {
      "status": "Verified",
      "integrity": "Valid",
      "method": "BLS-BN128",
      "details": "e(sig, g2) == e(H(m), pk)"
    }
    ```
