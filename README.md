# IdentityProof Protocol 🛡️

### Face-Based Web Discovery + Blockchain Integrity Verification

IdentityProof Protocol is an end-to-end Python pipeline that takes a face image, performs a genuine reverse-image web search, evaluates discovered candidate images using face embeddings, creates a cryptographic fingerprint of the discovered web record, and anchors that fingerprint on an EVM-compatible blockchain.

The system is designed as a local CLI application. No website or hosted frontend is required.

---

## 🚀 What the Project Does

The complete pipeline is:

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