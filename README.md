# 🛡️ IdentityProof Protocol

### Face-Based Web Discovery + Blockchain Integrity Verification

IdentityProof Protocol is an end-to-end **Python CLI application** that combines face recognition, genuine reverse-image web search, candidate face verification, cryptographic fingerprinting, and blockchain integrity verification.

The system takes a face image as input, discovers potentially matching images from the web, evaluates candidate images using **SFace face embeddings**, creates a canonical record of the discovered web evidence, generates a **SHA-256 cryptographic fingerprint**, and anchors that fingerprint on an **EVM-compatible blockchain**.

The stored blockchain fingerprint can later be retrieved and compared with a newly calculated fingerprint to determine whether the recorded web evidence has changed.

---

## 🚀 Project Overview

IdentityProof follows a complete investigation and verification pipeline:

```text
FACE IMAGE
    ↓
Face Detection
    ↓
SFace Face Embedding
    ↓
Genuine Reverse Image Search
    ↓
Web / Social Media Candidates
    ↓
Candidate Face Verification
    ↓
Best-Matching Candidate
    ↓
Canonical Web Record
    ↓
SHA-256 Fingerprint
    ↓
Blockchain Transaction
    ↓
Read On-Chain Record
    ↓
Recalculate SHA-256
    ↓
MATCH ✅ / TAMPERED ❌

The project is designed as a local command-line application and does not require a hosted website or frontend.

✨ Key Features
👤 Face Detection

Detects and extracts the face from the input image before performing face comparison.

🧠 SFace Face Embeddings

Uses the SFace face recognition model to convert detected faces into numerical embeddings.

These embeddings are used to compare the input face with faces found in discovered candidate images.

🌐 Genuine Reverse Image Search

Performs a genuine reverse-image web search to discover potentially relevant online references.

Possible results may include:

Public web pages
Profile pages
Social media references
Public images
Related online records
🔎 Candidate Face Verification

Discovered candidate images are evaluated using face embeddings.

The system compares:

Input Face
    ↓
SFace Embedding
    ↓
Candidate Face Embedding
    ↓
Similarity Comparison
    ↓
Candidate Match Score

The candidate with the strongest similarity can then be selected for further processing.

📄 Canonical Web Record

The selected web result is converted into a structured and deterministic record.

A canonical record may contain:

Candidate URL
Image URL
Page title
Match score
Search metadata
Relevant evidence
🔐 SHA-256 Cryptographic Fingerprint

The canonical web record is converted into a SHA-256 hash.

Canonical Web Record
        ↓
      SHA-256
        ↓
Cryptographic Fingerprint

The fingerprint provides a compact representation of the recorded evidence.

⛓️ Blockchain Anchoring

The generated fingerprint is anchored on an EVM-compatible blockchain.

The blockchain stores the integrity fingerprint rather than the original face image or complete webpage.

🔍 On-Chain Integrity Verification

The system can retrieve the stored fingerprint from the blockchain and compare it with a newly calculated SHA-256 fingerprint.

Stored Blockchain Hash
          │
          ↓
      Comparison
          ↑
          │
Recalculated SHA-256

Result:

MATCH ✅

or:

TAMPERED ❌
🏗️ System Architecture
                         ┌────────────────────┐
                         │    Input Image     │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │   Face Detection   │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │  SFace Embedding  │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Reverse Image      │
                         │ Search             │
                         └─────────┬──────────┘
                                   │
                                   ▼
                    ┌────────────────────────────┐
                    │ Web / Social Media         │
                    │ Candidate Images           │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │ Candidate Face Verification│
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │ Best-Matching Candidate    │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │ Canonical Web Record       │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │ SHA-256 Fingerprint        │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │ EVM-Compatible Blockchain  │
                    │ Integrity Anchor           │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │ On-Chain Verification      │
                    └─────────────┬──────────────┘
                                  │
                             ┌────┴────┐
                             ▼         ▼
                         MATCH ✅   TAMPERED ❌
🔄 Complete Workflow
Step 1 — Input Face Image

The user provides a face image through the local CLI application.

Input Image
    ↓
Face Detection
Step 2 — Face Detection

The system detects the face region from the input image.

Step 3 — Generate SFace Embedding

The detected face is processed using SFace to generate a numerical face embedding.

Detected Face
     ↓
   SFace
     ↓
Face Embedding
Step 4 — Reverse Image Search

The system performs a genuine reverse-image search to discover potentially related online images and web pages.

Step 5 — Collect Candidates

The discovered results are collected and prepared for candidate verification.

Step 6 — Candidate Face Verification

Faces from candidate images are detected and compared against the original face embedding.

Input Embedding
      +
Candidate Embedding
      ↓
Similarity Calculation
      ↓
Match Score
Step 7 — Select Candidate

The candidate with the strongest matching evidence is selected for the next stage.

Step 8 — Create Canonical Web Record

The selected web information is normalized into a canonical record.

Step 9 — Generate SHA-256 Fingerprint

The canonical record is hashed using SHA-256.

Step 10 — Blockchain Anchoring

The generated fingerprint is stored on an EVM-compatible blockchain.

Step 11 — Read Blockchain Record

The stored fingerprint is retrieved from the blockchain.

Step 12 — Recalculate Fingerprint

The current web record is canonicalized again and hashed.

Step 13 — Integrity Verification

The newly calculated fingerprint is compared with the blockchain fingerprint.

Same Hash
    ↓
MATCH ✅
Different Hash
    ↓
TAMPERED ❌
🧩 Technology Stack
Component	Technology
Programming Language	Python
Face Detection	OpenCV
Face Recognition	SFace
Face Embeddings	SFace
Reverse Image Search	Reverse Image Search Service
Cryptographic Hashing	SHA-256
Blockchain	EVM-Compatible Blockchain
Blockchain Interaction	Web3 / Ethereum-Compatible Tools
Configuration	Environment Variables
Application Type	Local CLI
📂 Project Structure
IdentityProof/
│
├── backend/
│   ├── face_detection.py
│   ├── face_embedding.py
│   ├── reverse_search.py
│   ├── candidate_verification.py
│   ├── canonical_record.py
│   ├── hashing.py
│   ├── blockchain.py
│   └── verification.py
│
├── models/
│   └── SFace/
│
├── data/
│   ├── input/
│   ├── candidates/
│   └── results/
│
├── screenshots/
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── main.py
⚙️ Installation
1. Clone the Repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd IdentityProof
2. Create a Virtual Environment
python -m venv venv
3. Activate the Virtual Environment
Windows
venv\Scripts\activate
Linux / macOS
source venv/bin/activate
4. Install Dependencies
pip install -r requirements.txt
🔑 Environment Configuration

Create a .env file in the project root.

Example:

RPC_URL=YOUR_EVM_RPC_URL
PRIVATE_KEY=YOUR_WALLET_PRIVATE_KEY
CONTRACT_ADDRESS=YOUR_CONTRACT_ADDRESS

Depending on the reverse-image search implementation, additional service credentials may also be required.

⚠️ Security Notice

Never commit sensitive information to GitHub.

Do not expose:

Private wallet keys
API keys
RPC credentials
Authentication tokens
Other secrets

Make sure .env is included in .gitignore.

▶️ Running the Application

The application is designed as a local CLI.

Run:

python main.py

Example interaction:

========================================
       IDENTITYPROOF PROTOCOL
========================================

Enter face image path:
> data/input/person.jpg

[1] Detecting face...
[2] Generating SFace embedding...
[3] Performing reverse image search...
[4] Collecting candidate images...
[5] Verifying candidate faces...
[6] Selecting best candidate...
[7] Creating canonical web record...
[8] Generating SHA-256 fingerprint...
[9] Anchoring fingerprint on blockchain...
[10] Reading blockchain record...
[11] Verifying integrity...

RESULT: MATCH ✅
🔐 Integrity Verification

IdentityProof uses deterministic hashing to verify the integrity of discovered web evidence.

Step 1 — Create Canonical Record

Relevant information is normalized into a canonical structure.

Candidate URL
+
Image URL
+
Page Metadata
+
Match Information
+
Relevant Evidence
Step 2 — Generate SHA-256 Fingerprint
Canonical Web Record
        ↓
      SHA-256
        ↓
Cryptographic Fingerprint
Step 3 — Store Fingerprint

The fingerprint is anchored on the blockchain.

Step 4 — Retrieve Fingerprint

During verification, the original fingerprint is read from the blockchain.

Step 5 — Recalculate Fingerprint

The current web record is processed again using the same canonicalization and SHA-256 process.

Step 6 — Compare
Blockchain Fingerprint
          │
          ▼
      Comparison
          ▲
          │
Current Fingerprint

If they match:

MATCH ✅

If they differ:

TAMPERED ❌
⛓️ Blockchain Integrity Model

The blockchain acts as the integrity and provenance layer.

The system does not need to store the complete evidence directly on-chain.

Instead, the evidence is processed locally and represented by a cryptographic fingerprint.

                    OFF-CHAIN
┌──────────────────────────────────────┐
│ Face Image                           │
│ Reverse Search Results               │
│ Candidate Images                     │
│ Candidate Information                │
│ Canonical Web Record                 │
└───────────────────┬──────────────────┘
                    │
                    ▼
                 SHA-256
                    │
                    ▼
          Cryptographic Fingerprint
                    │
                    ▼
                 ON-CHAIN
┌──────────────────────────────────────┐
│ Integrity Fingerprint                │
│ Transaction Information              │
│ Blockchain Record                    │
└──────────────────────────────────────┘

This approach keeps the blockchain record compact while providing a tamper-evident reference to the original evidence state.

🧠 Why SFace Embeddings?

Traditional pixel-level image comparison can be affected by:

Different lighting conditions
Camera angles
Image resolution
Background changes
Image compression
Minor visual differences

Face embeddings provide a numerical representation of facial features that can be compared between the input image and candidate images.

Input Face
    ↓
SFace
    ↓
Embedding Vector
    ↓
Similarity Comparison
    ↓
Candidate Match Score

However, face similarity should be treated as supporting evidence, not as absolute proof of a person's real-world identity.

🔎 Candidate Verification

The candidate verification stage evaluates discovered images against the original face.

Example:

----------------------------------------
Candidate Verification
----------------------------------------

Candidate 1    Similarity: 0.82
Candidate 2    Similarity: 0.94
Candidate 3    Similarity: 0.76
Candidate 4    Similarity: 0.69

Best Candidate:
Candidate 2
----------------------------------------

The exact similarity threshold and scoring method depend on the implementation and should be calibrated using appropriate evaluation data.

📄 Canonical Web Record

The canonical web record provides a deterministic representation of the evidence that is being fingerprinted.

Example:

{
    "candidate_url": "...",
    "image_url": "...",
    "page_title": "...",
    "match_score": "...",
    "metadata": "...",
    "evidence": "..."
}

The canonicalization process ensures that the same underlying record produces the same SHA-256 fingerprint when processed consistently.

📊 Example Output
----------------------------------------
IdentityProof Investigation
----------------------------------------

Input Image:
data/input/person.jpg

Face Detected:
YES

Reverse Search:
COMPLETED

Candidates Found:
12

Candidate Verification:
----------------------------------------
Candidate 1    Similarity: 0.82
Candidate 2    Similarity: 0.94
Candidate 3    Similarity: 0.76
Candidate 4    Similarity: 0.69
----------------------------------------

Selected Candidate:
https://example.com/profile

Canonical Record:
Generated

SHA-256:
a91c8d...7f21

Blockchain Transaction:
0x....

On-Chain Hash:
a91c8d...7f21

Integrity Status:
MATCH ✅
🛡️ Security Considerations

IdentityProof is designed with several security considerations:

Sensitive credentials are stored through environment variables.
Private keys are excluded from source control.
Face images can be processed locally.
Blockchain records contain fingerprints rather than raw images.
SHA-256 is used for cryptographic integrity verification.
Candidate similarity is treated as supporting evidence.
Web evidence may change over time.
Blockchain records provide a persistent reference to the fingerprint that was originally anchored.
⚠️ Limitations
Reverse Search Dependency

The quality and coverage of discovered candidates depend on the reverse-image search provider and the web sources accessible to it.

Face Recognition Limitations

Face matching can be affected by:

Poor image quality
Occlusion
Extreme viewing angles
Lighting differences
Low-resolution images
Similar-looking individuals
Dynamic Web Content

Web pages can change after an investigation.

If the current canonical record differs from the previously anchored record, the resulting SHA-256 fingerprint will also differ.

Blockchain Costs

Depending on the selected EVM network, blockchain transactions may require gas fees.

Identity Interpretation

A high face similarity score does not independently establish a person's identity.

The output should be interpreted as investigative evidence rather than an authoritative identity determination.

Search Coverage

No reverse-image search system can guarantee discovery of every instance of an image or person on the public web.

🎯 Project Objectives

The primary objectives of IdentityProof are:

Detect a face from an input image.
Generate a face embedding using SFace.
Discover potential web references using reverse-image search.
Collect candidate images and web records.
Verify candidate faces using embedding similarity.
Select the strongest candidate evidence.
Create a canonical web record.
Generate a SHA-256 cryptographic fingerprint.
Anchor the fingerprint on an EVM-compatible blockchain.
Retrieve the on-chain fingerprint.
Recalculate the current fingerprint.
Compare both fingerprints to detect changes.
📌 Project Highlights
✓ End-to-End Python Pipeline
✓ Face Detection
✓ SFace Face Recognition
✓ Face Embedding Comparison
✓ Genuine Reverse Image Search
✓ Web Evidence Discovery
✓ Candidate Face Verification
✓ Best-Match Candidate Selection
✓ Canonical Web Records
✓ SHA-256 Cryptographic Fingerprinting
✓ EVM Blockchain Anchoring
✓ On-Chain Integrity Verification
✓ Tamper Detection
✓ Local CLI Application
✓ No Hosted Frontend Required
🔮 Future Enhancements
🚀 V2 — Advanced Investigation
Multiple reverse-image search providers
Improved candidate ranking
Multi-face image handling
Better candidate filtering
Evidence confidence scoring
Automated investigation reports
More detailed search metadata
⛓️ V3 — Advanced Blockchain
Smart-contract based evidence registry
Multiple EVM network support
Evidence timestamps
Evidence versioning
Merkle-tree based evidence batches
Decentralized storage integration
🤖 V4 — Investigation Intelligence
Automated evidence correlation
Web-page change monitoring
Historical evidence tracking
Evidence graph visualization
AI-generated investigation summaries
Automated evidence reports
🧪 Testing

The project can be tested using controlled images and known web records.

Testing should cover:

✓ Face Detection
✓ Face Embedding Generation
✓ Reverse Search
✓ Candidate Extraction
✓ Candidate Face Matching
✓ Canonical Record Generation
✓ SHA-256 Generation
✓ Blockchain Transaction
✓ On-Chain Retrieval
✓ Integrity Verification
✓ Tampered Record Detection

A useful integrity test is:

Original Record
      ↓
Generate Hash
      ↓
Store On-Chain
      ↓
Read Hash
      ↓
Recalculate
      ↓
MATCH ✅

Then modify the canonical record:

Modified Record
      ↓
Generate New Hash
      ↓
Compare With On-Chain Hash
      ↓
TAMPERED ❌
📚 Responsible Use

IdentityProof deals with face images and online information. It should therefore be used responsibly.

The project is intended for:

Educational purposes
Cybersecurity research
Digital evidence research
Demonstration of blockchain integrity
Controlled investigation workflows

Users should respect applicable:

Privacy laws
Biometric-data regulations
Copyright rules
Website terms of service
Data protection requirements

Do not use the system to harass, impersonate, surveil, or make unsupported claims about individuals.

📄 License

This project is intended for educational, research, and demonstration purposes.

Use the project responsibly and in accordance with applicable laws, privacy requirements, biometric-data regulations, copyright rules, and third-party service terms
