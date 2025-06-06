🔐 Secure Simulated Data Sharing with Fine-Grained Access Control and Integrity Auditing in a Terminal–Edge–Cloud Architecture

🧠 Objective
To implement a simulated, fully software-based version of the data-sharing protocol proposed in the referenced research paper. The system features:

Lightweight encryption

CP-ABE-based fine-grained access control

Simulated integrity auditing using homomorphic signatures

The goal is to improve inefficiencies in prior schemes while keeping the system modular and efficient.

🏗️ System Architecture
Modules Overview
1. Terminal Device (DO Simulation)
Generates mock data (e.g., temperature, video logs)

Encrypts data using AES (lightweight encryption)

2. Edge Server (ES Simulation)
Decrypts AES-encrypted data

Re-encrypts using CP-ABE with defined access policies

Signs data blocks using simulated homomorphic signature logic

3. Cloud Server (CSP Simulation)
Stores the encrypted data and signature set

Responds to integrity audit challenges from the TPA

4. Third-Party Auditor (TPA)
Sends audit challenges and verifies proofs

Validates data integrity using a challenge-response model

5. Data User (DU)
Requests data

Gains access if attributes satisfy the CP-ABE policy

Decrypts the data accordingly

🛠️ Tools & Technologies

| Component            | Technology/Library                         |
| -------------------- | ------------------------------------------ |
| Programming Language | Python                                     |
| AES Encryption       | `cryptography` or `pycrypto`               |
| CP-ABE               | `charm-crypto` or custom implementation    |
| Integrity Signatures | Hash + modular exponentiation (mock HS)    |
| Storage              | Local filesystem / SQLite / JSON files     |
| Config Management    | JSON configs for users and access policies |

✨ Key Features

✅ Lightweight symmetric encryption at terminal

✅ CP-ABE-based fine-grained access at edge

✅ Homomorphic signature-based integrity auditing

✅ No blockchain; improved key management

✅ No ZK-proofs; uses efficient challenge–response mechanism

✅ Fully modular and software-driven

🎯 Outcomes

✅ A Python-based simulation showing secure data flow from terminal to cloud

✅ Attribute-controlled access and decryption using CP-ABE policies

✅ An audit system verifying integrity with simplified cryptographic logic

✅ Visual/console output displaying:

Data access granted/denied

Audit pass/failure status


