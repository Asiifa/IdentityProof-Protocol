# 🛡️ IdentityProof Protocol

### Face-Based Web Discovery & Blockchain Integrity Verification

IdentityProof Protocol is an end-to-end **Python-based CLI application** that combines face detection, face embedding comparison, reverse-image web search, cryptographic fingerprinting, and blockchain-based integrity verification.

The system processes an input face image, discovers potentially relevant online image references, evaluates candidate images using SFace face embeddings, generates a canonical record of the discovered web evidence, and anchors its SHA-256 fingerprint on an EVM-compatible blockchain.

The blockchain fingerprint can subsequently be retrieved and compared against a newly generated fingerprint to identify changes in the recorded evidence.

> **Project Type:** Python CLI Application  
> **Version:** 1.0.0  
> **Primary Focus:** Computer Vision, Digital Evidence, Cryptography & Blockchain

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [How It Works](#-how-it-works)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Environment Configuration](#-environment-configuration)
- [Running the Application](#-running-the-application)
- [Integrity Verification](#-integrity-verification)
- [Blockchain Integrity Model](#-blockchain-integrity-model)
- [Example Output](#-example-output)
- [Security & Privacy](#-security--privacy)
- [Limitations](#-limitations)
- [Testing](#-testing)
- [Future Enhancements](#-future-enhancements)
- [Responsible Use](#-responsible-use)
- [License](#-license)

---

## 🚀 Overview

IdentityProof Protocol explores how computer vision, web discovery, cryptographic hashing, and blockchain technology can work together in a digital evidence verification workflow.

The application follows a structured investigation pipeline:

```text
Input Face Image
       |
       v
  Face Detection
       |
       v
 SFace Embedding
       |
       v
 Reverse Image Search
       |
       v
 Web Image Candidates
       |
       v
Candidate Face Comparison
       |
       v
  Candidate Selection
       |
       v
  Canonical Web Record
       |
       v
   SHA-256 Hashing
       |
       v
 Blockchain Anchoring
       |
       v
 On-Chain Verification
       |
       v
 MATCH / TAMPERED
```

The project is designed as a local command-line application and does not require a hosted website or frontend.

### Project Objectives

- Detect faces from input images using computer vision.
- Generate numerical face embeddings using SFace.
- Discover potentially relevant online image references through reverse-image search.
- Compare candidate faces using embedding similarity.
- Organize discovered information into canonical web records.
- Generate SHA-256 cryptographic fingerprints.
- Anchor evidence fingerprints on an EVM-compatible blockchain.
- Retrieve previously stored blockchain fingerprints.
- Verify the integrity of recorded evidence.

---

## ✨ Key Features

### 👤 Face Detection

Uses OpenCV to detect and extract facial regions from the provided input image.

### 🧠 SFace Face Embeddings

Uses the SFace face recognition model to convert detected facial regions into numerical embedding vectors.

These embeddings support similarity comparisons between the input image and candidate images.

### 🌐 Reverse Image Search

Integrates a reverse-image search service to discover potentially relevant online image references.

Possible results include:

- Public web pages
- Public image references
- Profile pages
- Social media references
- Other accessible online records

Search coverage depends on the selected provider and its accessible sources.

### 🔎 Candidate Face Verification

Evaluates discovered candidate images using face embeddings.

The comparison workflow:

```text
Input Face
    |
    v
SFace Embedding
    |
    v
Candidate Face Detection
    |
    v
Candidate Embedding
    |
    v
Similarity Comparison
    |
    v
Candidate Match Score
```

The similarity score is supporting evidence and must not be interpreted as definitive proof of identity.

### 📄 Canonical Web Records

Converts selected web information into a structured and deterministic record.

A canonical record may contain:

- Candidate URL
- Image URL
- Page title
- Match score
- Search metadata
- Relevant evidence

### 🔐 SHA-256 Cryptographic Fingerprinting

Generates a SHA-256 fingerprint from the canonical web record.

```text
Canonical Web Record
        |
        v
     SHA-256
        |
        v
Cryptographic Fingerprint
```

This fingerprint represents the recorded evidence at the time it was processed.

### ⛓️ Blockchain Anchoring

Anchors the generated fingerprint on an EVM-compatible blockchain.

The blockchain stores the integrity fingerprint rather than the original face image or complete webpage.

### 🔍 On-Chain Integrity Verification

Retrieves the stored blockchain fingerprint and compares it against a newly calculated fingerprint.

Possible outcomes:

- **MATCH:** Both fingerprints are identical.
- **TAMPERED:** The fingerprints differ.

---

## 🏗️ System Architecture

The application is divided into independent processing stages.

```text
                  INPUT IMAGE
                       |
                       v
              +------------------+
              |  Face Detection  |
              +------------------+
                       |
                       v
              +------------------+
              | SFace Embedding  |
              +------------------+
                       |
                       v
              +------------------+
              | Reverse Image    |
              | Search           |
              +------------------+
                       |
                       v
              +------------------+
              | Web Image        |
              | Candidates       |
              +------------------+
                       |
                       v
              +------------------+
              | Candidate Face   |
              | Verification     |
              +------------------+
                       |
                       v
              +------------------+
              | Candidate        |
              | Selection        |
              +------------------+
                       |
                       v
              +------------------+
              | Canonical Web    |
              | Record           |
              +------------------+
                       |
                       v
              +------------------+
              | SHA-256          |
              | Fingerprinting   |
              +------------------+
                       |
                       v
              +------------------+
              | EVM Blockchain   |
              | Anchoring        |
              +------------------+
                       |
                       v
              +------------------+
              | On-Chain         |
              | Verification     |
              +------------------+
                       |
                 +-----+-----+
                 |           |
                 v           v
               MATCH     TAMPERED
```

### Architectural Components

| Component | Responsibility |
|---|---|
| Face Recognition | Face detection and embedding generation |
| Reverse Search | Online image discovery |
| Candidate Verification | Candidate face comparison |
| Evidence Processing | Canonical web record generation |
| Cryptographic Layer | SHA-256 fingerprint generation |
| Blockchain Layer | Fingerprint anchoring and retrieval |
| Main Application | Coordinates the complete CLI workflow |

---

## 🔄 How It Works

The complete workflow consists of the following stages.

**Step 1 — Input Face Image**

The user provides an image through the local CLI application.

**Step 2 — Face Detection**

OpenCV detects the face region from the input image.

**Step 3 — Generate SFace Embedding**

The detected face is processed using SFace to generate a numerical embedding.

**Step 4 — Reverse Image Search**

The application submits the image to the configured reverse-image search service.

**Step 5 — Collect Candidates**

Potentially relevant image references and web results are collected.

**Step 6 — Candidate Face Verification**

Detected faces in candidate images are compared with the input embedding.

**Step 7 — Candidate Selection**

Candidate similarity and available evidence are evaluated for further investigation.

**Step 8 — Create Canonical Web Record**

Selected web information is normalized into a structured record.

**Step 9 — Generate SHA-256 Fingerprint**

The canonical record is converted into a cryptographic fingerprint.

**Step 10 — Blockchain Anchoring**

The fingerprint is submitted to the configured EVM-compatible blockchain.

**Step 11 — Retrieve Blockchain Record**

The previously stored fingerprint is retrieved.

**Step 12 — Recalculate Fingerprint**

The current canonical record is processed again using the same hashing procedure.

**Step 13 — Verify Integrity**

The newly generated fingerprint is compared with the blockchain fingerprint.

```text
Same Fingerprint
       |
       v
     MATCH

Different Fingerprint
       |
       v
   TAMPERED
```

---

## 🧩 Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Computer Vision | OpenCV |
| Face Recognition | SFace |
| Face Embeddings | SFace |
| Reverse Image Search | Reverse Image Search Service |
| Cryptographic Hashing | SHA-256 |
| Blockchain | EVM-Compatible Blockchain |
| Blockchain Integration | Web3 / Ethereum-Compatible Tools |
| Configuration | Environment Variables |
| Application Type | Local CLI |

---

## 📂 Project Structure

The project follows a modular structure that separates face recognition, web discovery, evidence processing, and blockchain operations.

```text
IdentityProof/
│
├── backend/
│   │
│   ├── face_recognition/
│   │   ├── __init__.py
│   │   ├── face_detection.py
│   │   ├── face_embedding.py
│   │   └── candidate_verification.py
│   │
│   ├── reverse_search/
│   │   ├── __init__.py
│   │   └── reverse_search.py
│   │
│   ├── evidence/
│   │   ├── __init__.py
│   │   └── canonical_record.py
│   │
│   ├── blockchain/
│   │   ├── __init__.py
│   │   ├── hashing.py
│   │   ├── blockchain.py
│   │   └── verification.py
│   │
│   └── __init__.py
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
├── tests/
│   ├── test_face_detection.py
│   ├── test_candidate_verification.py
│   ├── test_hashing.py
│   └── test_blockchain.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── main.py
```

### Directory Responsibilities

| Directory / File | Description |
|---|---|
| `backend/` | Core application modules |
| `face_recognition/` | Face detection, embedding generation and candidate verification |
| `reverse_search/` | Reverse-image search integration |
| `evidence/` | Canonical web record processing |
| `blockchain/` | Hashing, blockchain interaction and integrity verification |
| `models/SFace/` | SFace model files |
| `data/input/` | Input images |
| `data/candidates/` | Collected candidate images |
| `data/results/` | Generated investigation results |
| `screenshots/` | Application screenshots |
| `tests/` | Automated test modules |
| `.env.example` | Example environment configuration |
| `requirements.txt` | Python dependencies |
| `main.py` | Application entry point |

> **Note:** This is the intended modular organization. Ensure that the actual repository contains these files before presenting the tree as the final implemented structure. The test files are proposed test modules, not a claim that all tests have already been implemented.

---

## ⚙️ Installation & Setup

### Prerequisites

Make sure the following are available:

- Python
- Git
- pip
- An EVM-compatible blockchain RPC endpoint
- A configured reverse-image search service

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate into the project:

```bash
cd IdentityProof
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the Environment

Create a `.env` file in the project root and configure the required credentials.

Refer to the [Environment Configuration](#-environment-configuration) section.

---

## 🔑 Environment Configuration

The application uses environment variables to manage external service credentials and blockchain configuration.

Create a `.env` file:

```env
RPC_URL=YOUR_EVM_RPC_URL
PRIVATE_KEY=YOUR_WALLET_PRIVATE_KEY
CONTRACT_ADDRESS=YOUR_CONTRACT_ADDRESS
```

Additional environment variables may be required depending on the reverse-image search provider and blockchain implementation.

### Security Recommendations

- Never commit `.env` to GitHub.
- Never expose private wallet keys.
- Never publish API credentials.
- Use a dedicated development wallet.
- Prefer a blockchain test network during development.
- Keep `.env.example` free of actual credentials.

---

## ▶️ Running the Application

Activate your virtual environment and execute:

```bash
python main.py
```

### Example CLI Interaction

```text
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
[6] Selecting candidate evidence...
[7] Creating canonical web record...
[8] Generating SHA-256 fingerprint...
[9] Anchoring fingerprint on blockchain...
[10] Reading blockchain record...
[11] Verifying integrity...

RESULT: MATCH
```

*The above represents an example interaction. Actual output depends on the configured services and implementation.*

---

## 🔐 Integrity Verification

Integrity verification is one of the central components of IdentityProof.

It uses deterministic canonicalization and SHA-256 hashing to check whether a recorded evidence representation matches its previously anchored fingerprint.

### Verification Process

**1. Create Canonical Record**

Relevant web information is normalized into a structured record.

**2. Generate SHA-256 Fingerprint**

The canonical record is processed using SHA-256.

**3. Store Fingerprint**

The generated fingerprint is anchored on the blockchain.

**4. Retrieve Fingerprint**

During verification, the previously stored fingerprint is retrieved.

**5. Recalculate Fingerprint**

The current record is canonicalized and hashed using the same procedure.

**6. Compare Fingerprints**

```text
Blockchain Fingerprint
          |
          v
       Compare
          ^
          |
 Current Fingerprint
```

### Verification Results

| Condition | Result |
|---|---|
| Fingerprints match | MATCH |
| Fingerprints differ | TAMPERED |

A mismatch indicates that the current canonical record differs from the originally anchored record. It does not, by itself, establish why the difference occurred.

---

## ⛓️ Blockchain Integrity Model

IdentityProof uses blockchain as an integrity and provenance layer.

Instead of storing complete images, webpages, or investigation records directly on-chain, the system stores their cryptographic fingerprint.

### Off-Chain Storage

- Input face image
- Reverse-image search results
- Candidate images
- Candidate information
- Canonical web record

### On-Chain Storage

- Integrity fingerprint
- Transaction information
- Blockchain record

```text
             OFF-CHAIN
    +---------------------------+
    | Input Image               |
    | Search Results            |
    | Candidate Information     |
    | Canonical Web Record      |
    +-------------+-------------+
                  |
                  v
             SHA-256
                  |
                  v
       Cryptographic Fingerprint
                  |
                  v
              ON-CHAIN
    +---------------------------+
    | Integrity Fingerprint     |
    | Transaction Information   |
    | Blockchain Record         |
    +---------------------------+
```

This approach keeps the blockchain record compact while providing a tamper-evident reference to the evidence state that was originally recorded.

---

## 📊 Example Output

The following is an illustrative example of an investigation result.

```text
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

----------------------------------------
Candidate Verification
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
MATCH

----------------------------------------
```

*Candidate scores, URLs, hashes, and transaction values above are illustrative placeholders, not verified live results.*

---

## 🔒 Security & Privacy

IdentityProof handles face images and potentially sensitive online information. Security and privacy must therefore be considered throughout the application.

The project incorporates or aims to incorporate the following safeguards:

- Environment variables for sensitive credentials.
- Exclusion of private keys from source control.
- Local processing of input images where supported.
- Blockchain storage of fingerprints rather than raw images.
- SHA-256 for cryptographic integrity verification.
- Candidate similarity treated as supporting evidence.
- Responsible handling of collected web information.

Sensitive biometric data and investigation records should be stored securely and retained only as long as necessary.

---

## ⚠️ Limitations

### Reverse Search Dependency

The quality and coverage of discovered candidates depend on the reverse-image search provider and the web sources accessible to it.

No provider guarantees discovery of every online reference.

### Face Recognition Limitations

Face matching can be affected by:

- Poor image quality
- Occlusion
- Extreme viewing angles
- Lighting differences
- Low resolution
- Similar-looking individuals

A high similarity score does not independently establish a person's identity.

### Dynamic Web Content

Webpages and online images can change over time.

If the current canonical record differs from the originally anchored record, its SHA-256 fingerprint will also differ.

### Blockchain Costs

Depending on the selected EVM network, blockchain transactions may require gas fees.

### Identity Interpretation

The system provides investigative evidence, not authoritative identity verification.

### Search Coverage

Reverse-image search cannot guarantee complete coverage of the public web or private and inaccessible platforms.

---

## 🧪 Testing

Testing should cover the individual components and the complete verification workflow.

### Recommended Test Coverage

| Component | Test Scenario |
|---|---|
| Face Detection | Detect a face in a valid image |
| Face Embedding | Generate an embedding |
| Candidate Verification | Compare candidate face embeddings |
| Reverse Search | Verify search integration |
| Canonical Record | Generate a consistent record |
| SHA-256 | Generate deterministic fingerprints |
| Blockchain | Anchor and retrieve a fingerprint |
| Integrity Verification | Compare stored and recalculated fingerprints |

### Example Integrity Test

```text
Original Record
       |
       v
Generate Hash
       |
       v
Store On-Chain
       |
       v
Retrieve Hash
       |
       v
Recalculate
       |
       v
    MATCH
```

Then modify the canonical record:

```text
Modified Record
       |
       v
Generate New Hash
       |
       v
Compare With Original Hash
       |
       v
   TAMPERED
```

---

## 🔮 Future Enhancements

### V2 — Advanced Investigation

- Multiple reverse-image search providers.
- Improved candidate ranking.
- Multi-face image handling.
- Better candidate filtering.
- Evidence confidence scoring.
- Automated investigation reports.
- More detailed search metadata.

### V3 — Advanced Blockchain

- Smart-contract-based evidence registry.
- Multiple EVM network support.
- Evidence timestamps.
- Evidence versioning.
- Merkle-tree-based evidence batches.
- Decentralized storage integration.

### V4 — Investigation Intelligence

- Automated evidence correlation.
- Webpage change monitoring.
- Historical evidence tracking.
- Evidence graph visualization.
- AI-generated investigation summaries.
- Automated evidence reports.

---

## 🎯 Project Highlights

- End-to-end Python application.
- Computer vision-based face detection.
- SFace face recognition.
- Numerical face embedding comparison.
- Reverse-image web discovery.
- Candidate image verification.
- Canonical web evidence records.
- SHA-256 cryptographic fingerprinting.
- EVM-compatible blockchain integration.
- On-chain fingerprint retrieval.
- Evidence integrity verification.
- Tamper-evident record comparison.
- Modular application architecture.
- Local CLI execution.

---

## 🛡️ Responsible Use

IdentityProof is intended for educational purposes, cybersecurity research, digital evidence research, and blockchain integrity demonstrations.

Because the application processes biometric information and discovers online references, it must be used responsibly.

Users should:

- Obtain appropriate consent before processing another person's biometric information.
- Respect applicable privacy and data protection laws.
- Follow website terms of service.
- Respect copyright and intellectual property rights.
- Avoid unauthorized surveillance, harassment, or impersonation.
- Never treat face similarity as conclusive proof of identity.
- Avoid publishing sensitive personal information without authorization.

The application should be used only in lawful, consent-based, and appropriately controlled investigation workflows.

---

## 📄 License

No open-source license has been specified for this project yet.

Until a license is added to the repository, the source code remains subject to the default copyright protections. See [Choose an open-source license](https://choosealicense.com/) when deciding how to distribute the project.

---

**IdentityProof Protocol — Connecting Computer Vision, Digital Evidence & Blockchain Integrity.**
