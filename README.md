�
�
 Project Title: 
Secure Simulated Data Sharing with Fine-Grained Access Control and Integrity Auditing 
in a Terminal–Edge–Cloud Architecture 
�
�
 Objective: 
To implement a simulated, fully software-based version of the data-sharing protocol proposed in 
the referenced research paper. The system will feature lightweight encryption, CP-ABE-based 
fine-grained access control, and a simulated integrity auditing mechanism using homomorphic 
signatures — all while improving upon inefficiencies noted in previous schemes. 
�
�
 System Architecture: 
Modules: 
1. Terminal Device (DO Simulation) 
○ Generates mock data (e.g., temperature, video logs). 
○ Encrypts data using AES (lightweight encryption). 
2. Edge Server (ES Simulation) 
○ Decrypts AES-encrypted data. 
○ Re-encrypts using CP-ABE with defined access policies. 
○ Signs data blocks using simulated homomorphic signature logic. 
3. Cloud Server (CSP Simulation) 
○ Stores the encrypted data and signature set. 
○ Responds to integrity audit challenges from the TPA. 
4. Third-Party Auditor (TPA) 
○ Sends audit challenges and verifies proofs. 
○ Validates data integrity using the challenge-response model. 
5. Data User (DU) 
○ Requests data. 
○ Gains access if attributes satisfy CP-ABE policy. 
○ Decrypts the data accordingly. 
�
�
 Tools & Technologies: 
Component 
Programming 
Language 
Encryption (PIPO-sim) 
Python 
Tool/Library 
AES via cryptography or pycrypto 
CP-ABE 
Integrity Signatures 
Storage 
Simulation Logic 
charm-crypto or custom logic 
Hash + modular exponentiation (mock HS) 
Local filesystem / SQLite / JSON files 
JSON configs for users and access sets 
�
�
 Key Features : 
● 
✅
 Lightweight symmetric encryption at terminal 
● 
✅
 CP-ABE-based fine-grained access at edge 
● 
✅
 Homomorphic signature-based integrity auditing 
● 
✅
 No blockchain; improved key management 
● 
✅
 No ZK-proofs; uses efficient challenge–response 
● 
✅
 Fully modular and software-driven 
�
�
 Outcomes: 
● A functional Python-based simulation demonstrating secure data flow from terminal to 
cloud. 
● Attribute-controlled access and decryption based on defined policies. 
● An audit system that verifies integrity of stored data using simplified cryptographic logic. 
● Visual or console-based output showing when access is granted/denied, and when audit 
passes/fails.
