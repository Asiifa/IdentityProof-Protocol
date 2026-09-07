import os
import json
import hashlib
import argparse

from web_search import search_image
from candidate_matcher import evaluate_candidates
from blockchain import (
    connect_blockchain,
    load_contract,
    anchor_hash,
    verify_hash
)


# ============================================================
# SETTINGS
# ============================================================

MATCH_THRESHOLD = 0.363

RECORD_FILE = "discovered_record.json"
TAMPERED_RECORD_FILE = "tampered_record.json"


# ============================================================
# BUILD CANONICAL RECORD
# ============================================================

def build_record(candidate):
    """
    Build the exact web record that will be fingerprinted.
    """

    return {
        "title": candidate.get(
            "title",
            ""
        ),

        "source": candidate.get(
            "source",
            ""
        ),

        "page_url": candidate.get(
            "page_url",
            ""
        ),

        "image_url": candidate.get(
            "image_url",
            ""
        )
    }


# ============================================================
# CREATE SHA-256
# ============================================================

def create_fingerprint(data):
    """
    Create deterministic SHA-256 fingerprint.
    """

    canonical_data = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )

    digest = hashlib.sha256(
        canonical_data.encode("utf-8")
    ).hexdigest()

    return canonical_data, digest


# ============================================================
# SAVE JSON RECORD
# ============================================================

def save_record(
    data,
    filename=RECORD_FILE
):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
            sort_keys=True
        )


# ============================================================
# TAMPER TEST
# ============================================================

def run_tamper_test(
    original_record,
    blockchain_hash
):

    print("\n==========================================")
    print("             TAMPER TEST")
    print("==========================================")

    # Make a copy
    tampered_record = dict(
        original_record
    )

    # Deliberately modify one field
    tampered_record["title"] = (
        tampered_record.get(
            "title",
            ""
        )
        + " [MODIFIED]"
    )

    save_record(
        tampered_record,
        TAMPERED_RECORD_FILE
    )

    _, tampered_hash = create_fingerprint(
        tampered_record
    )

    print(
        "\nOriginal / On-chain hash:"
    )

    print(
        blockchain_hash
    )

    print(
        "\nTampered data hash:"
    )

    print(
        tampered_hash
    )

    if tampered_hash == blockchain_hash:

        print(
            "\n❌ SECURITY CHECK FAILED"
        )

    else:

        print(
            "\n✅ TAMPER DETECTED"
        )

        print(
            "The modified record does not match "
            "the blockchain fingerprint."
        )

    print("==========================================")


# ============================================================
# MAIN PIPELINE
# ============================================================

def main(image_path, tamper_test=False):

    print("\n")
    print("============================================================")
    print("       FACE → WEB → BLOCKCHAIN VERIFICATION")
    print("============================================================")

    # ========================================================
    # STEP 1 — FACE + WEB SEARCH
    # ========================================================

    print("\n[1] Starting genuine web search...")

    lens_results = search_image(
        image_path
    )

    visual_matches = lens_results.get(
        "visual_matches",
        []
    )

    exact_matches = lens_results.get(
        "exact_matches",
        []
    )

    print(
        f"\n    Exact matches : "
        f"{len(exact_matches)}"
    )

    print(
        f"    Visual matches: "
        f"{len(visual_matches)}"
    )

    if not visual_matches:

        print(
            "\n❌ No web candidates were discovered."
        )

        return False

    # ========================================================
    # STEP 2 — FACE VERIFICATION
    # ========================================================

    print(
        "\n[2] Verifying discovered candidates "
        "with SFace..."
    )

    # Evaluate candidates
    candidates = visual_matches

    ranked_results = evaluate_candidates(
        image_path,
        candidates
    )

    if not ranked_results:

        print(
            "\n❌ No candidate images could be analyzed."
        )

        return False

    # Only candidates that pass our threshold
    verified_candidates = [
        result
        for result in ranked_results
        if result.get(
            "passes_threshold",
            False
        )
    ]

    if not verified_candidates:

        best = ranked_results[0]

        print(
            "\n============================================================"
        )

        print(
            "❌ NO VERIFIED WEB MATCH FOUND"
        )

        print(
            "============================================================"
        )

        print(
            f"\nBest candidate:"
        )

        print(
            f"Source       : "
            f"{best.get('source', 'N/A')}"
        )

        print(
            f"URL          : "
            f"{best.get('page_url', 'N/A')}"
        )

        print(
            f"Cosine score : "
            f"{best.get('cosine_score', 0):.4f}"
        )

        print(
            f"Threshold    : "
            f"{MATCH_THRESHOLD:.3f}"
        )

        print(
            "\nThe blockchain stage was NOT executed "
            "because no candidate passed face verification."
        )

        return False

    # ========================================================
    # STEP 3 — SELECT VERIFIED CANDIDATE
    # ========================================================

    verified_candidates.sort(
        key=lambda item: item[
            "cosine_score"
        ],
        reverse=True
    )

    best_candidate = (
        verified_candidates[0]
    )

    print(
        "\n============================================================"
    )

    print(
        "✅ VERIFIED CANDIDATE FOUND"
    )

    print(
        "============================================================"
    )

    print(
        f"\nTitle        : "
        f"{best_candidate.get('title', 'N/A')}"
    )

    print(
        f"Source       : "
        f"{best_candidate.get('source', 'N/A')}"
    )

    print(
        f"URL          : "
        f"{best_candidate.get('page_url', 'N/A')}"
    )

    print(
        f"Cosine score : "
        f"{best_candidate.get('cosine_score', 0):.4f}"
    )

    # ========================================================
    # STEP 4 — BUILD RECORD
    # ========================================================

    print(
        "\n[3] Creating canonical web record..."
    )

    record = build_record(
        best_candidate
    )

    save_record(
        record
    )

    print(
        "    ✓ Record saved to "
        f"{RECORD_FILE}"
    )

    # ========================================================
    # STEP 5 — SHA-256
    # ========================================================

    print(
        "\n[4] Creating SHA-256 fingerprint..."
    )

    canonical_data, fingerprint = (
        create_fingerprint(
            record
        )
    )

    print(
        "    ✓ SHA-256 created"
    )

    print(
        f"\n    Fingerprint:"
    )

    print(
        f"    {fingerprint}"
    )

    # ========================================================
    # STEP 6 — BLOCKCHAIN
    # ========================================================

    print(
        "\n[5] Connecting to blockchain..."
    )

    web3 = connect_blockchain()

    contract = load_contract(
        web3
    )

    print(
        "    ✓ Connected to Hardhat"
    )

    print(
        f"    Chain ID: "
        f"{web3.eth.chain_id}"
    )

    # --------------------------------------------------------
    # Check if the hash already exists
    # --------------------------------------------------------

    existing = verify_hash(
        web3,
        contract,
        fingerprint
    )

    if existing[0]:

        print(
            "\n⚠ Hash already exists."
        )

        print(
            "Using the existing blockchain record."
        )

        blockchain_hash = fingerprint

        print(
            f"\nSource already recorded:"
            f"\n{existing[3]}"
        )

    else:

        # ----------------------------------------------------
        # Store new hash
        # ----------------------------------------------------

        receipt = anchor_hash(
            web3,
            contract,
            fingerprint,
            best_candidate.get(
                "page_url",
                "unknown"
            )
        )

        print(
            "\n✓ New fingerprint anchored."
        )

        print(
            "Transaction hash:",
            receipt.transactionHash.hex()
        )

        blockchain_hash = fingerprint

    # ========================================================
    # STEP 7 — READ BLOCKCHAIN RECORD
    # ========================================================

    print(
        "\n[6] Reading blockchain record..."
    )

    on_chain = verify_hash(
        web3,
        contract,
        blockchain_hash
    )

    if not on_chain[0]:

        print(
            "\n❌ Blockchain verification failed."
        )

        return False

    # ========================================================
    # STEP 8 — RE-HASH DISCOVERED DATA
    # ========================================================

    print(
        "\n[7] Re-calculating fingerprint..."
    )

    with open(
        RECORD_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        current_record = json.load(
            file
        )

    _, recalculated_hash = (
        create_fingerprint(
            current_record
        )
    )

    print(
        "\n    On-chain hash:"
    )

    print(
        f"    {blockchain_hash}"
    )

    print(
        "\n    Re-calculated hash:"
    )

    print(
        f"    {recalculated_hash}"
    )

    # ========================================================
    # STEP 9 — FINAL VERIFICATION
    # ========================================================

    print(
        "\n============================================================"
    )

    if blockchain_hash == recalculated_hash:

        print(
            "✅ FINAL RESULT: VERIFIED"
        )

        print(
            "The discovered record matches "
            "the blockchain fingerprint."
        )

        verified = True

    else:

        print(
            "❌ FINAL RESULT: TAMPERED"
        )

        print(
            "The discovered record does not match "
            "the blockchain fingerprint."
        )

        verified = False

    print(
        "============================================================"
    )

    # ========================================================
    # OPTIONAL TAMPER TEST
    # ========================================================

    if tamper_test and verified:

        run_tamper_test(
            current_record,
            blockchain_hash
        )

    return verified


# ============================================================
# COMMAND-LINE ENTRY
# ============================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=(
            "End-to-end Face → Web → "
            "Blockchain verification pipeline"
        )
    )

    parser.add_argument(
        "--image",
        required=True,
        help="Path to input face image"
    )

    parser.add_argument(
        "--tamper-test",
        action="store_true",
        help="Run blockchain tamper test"
    )

    args = parser.parse_args()

    if not os.path.isfile(
        args.image
    ):

        print(
            f"\n❌ Image not found: "
            f"{args.image}"
        )

        raise SystemExit(1)

    try:

        success = main(
            args.image,
            args.tamper_test
        )

        if success:

            print(
                "\n🎉 PIPELINE COMPLETED SUCCESSFULLY."
            )

        else:

            print(
                "\n⚠️ PIPELINE DID NOT PRODUCE "
                "A VERIFIED MATCH."
            )

    except KeyboardInterrupt:

        print(
            "\n\nPipeline cancelled."
        )

    except Exception as error:

        print(
            "\n❌ PIPELINE ERROR:"
        )

        print(
            error
        )

        raise