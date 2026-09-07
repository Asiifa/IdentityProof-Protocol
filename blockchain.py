import json

from web3 import Web3


# ============================================================
# CONFIGURATION
# ============================================================

RPC_URL = "http://127.0.0.1:8545"

CONTRACT_ADDRESS = (
    "0x5FbDB2315678afecb367f032d93F642f64180aa3"
)


CONTRACT_FILE = (
    "artifacts/contracts/"
    "identity_anchor.sol/"
    "IdentityAnchor.json"
)


# ============================================================
# CONNECT TO HARDHAT
# ============================================================

def connect_blockchain():

    web3 = Web3(
        Web3.HTTPProvider(RPC_URL)
    )

    if not web3.is_connected():

        raise ConnectionError(
            "Could not connect to Hardhat blockchain."
        )

    return web3


# ============================================================
# LOAD CONTRACT
# ============================================================

def load_contract(web3):

    with open(
        CONTRACT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        contract_data = json.load(file)

    contract = web3.eth.contract(
        address=Web3.to_checksum_address(
            CONTRACT_ADDRESS
        ),
        abi=contract_data["abi"]
    )

    return contract


# ============================================================
# ANCHOR SHA-256
# ============================================================

def anchor_hash(
    web3,
    contract,
    sha256_hex,
    source
):

    account = web3.eth.accounts[0]

    # Convert 64-character SHA-256 hex
    # into exactly 32 bytes.
    data_hash = bytes.fromhex(
        sha256_hex
    )

    if len(data_hash) != 32:

        raise ValueError(
            "Invalid SHA-256 hash."
        )

    print("\n==========================================")
    print("          BLOCKCHAIN ANCHOR")
    print("==========================================")

    print(
        "\nAccount:",
        account
    )

    print(
        "SHA-256:",
        sha256_hex
    )

    print(
        "Source:",
        source
    )

    print(
        "\nSubmitting transaction..."
    )

    transaction_hash = (
        contract.functions.anchorProof(
            data_hash,
            source
        ).transact({
            "from": account
        })
    )

    receipt = (
        web3.eth.wait_for_transaction_receipt(
            transaction_hash
        )
    )

    print(
        "\n✓ Transaction confirmed"
    )

    print(
        "Transaction hash:",
        receipt.transactionHash.hex()
    )

    print(
        "Block number:",
        receipt.blockNumber
    )

    print("==========================================")

    return receipt


# ============================================================
# VERIFY ON BLOCKCHAIN
# ============================================================

def verify_hash(
    web3,
    contract,
    sha256_hex
):

    data_hash = bytes.fromhex(
        sha256_hex
    )

    result = contract.functions.verifyProof(
        data_hash
    ).call()

    is_verified = result[0]
    timestamp = result[1]
    submitter = result[2]
    source = result[3]

    print("\n==========================================")
    print("        ON-CHAIN VERIFICATION")
    print("==========================================")

    print(
        "\nVerified:",
        is_verified
    )

    print(
        "Timestamp:",
        timestamp
    )

    print(
        "Submitter:",
        submitter
    )

    print(
        "Source:",
        source
    )

    if is_verified:

        print(
            "\n✅ HASH FOUND ON BLOCKCHAIN"
        )

    else:

        print(
            "\n❌ HASH NOT FOUND"
        )

    print("==========================================")

    return result


# ============================================================
# MAIN TEST
# ============================================================

if __name__ == "__main__":

    web3 = connect_blockchain()

    print(
        "\n✓ Connected to Hardhat"
    )

    print(
        "Chain ID:",
        web3.eth.chain_id
    )

    contract = load_contract(
        web3
    )

    print(
        "✓ IdentityAnchor loaded"
    )

    # --------------------------------------------------------
    # Read fingerprint
    # --------------------------------------------------------

    from fingerprint import fingerprint_file

    _, sha256_hex = fingerprint_file(
        "discovered_record.json"
    )

    # --------------------------------------------------------
    # Read source URL
    # --------------------------------------------------------

    with open(
        "discovered_record.json",
        "r",
        encoding="utf-8"
    ) as file:

        record = json.load(file)

    source = record.get(
        "page_url",
        "unknown"
    )

    # --------------------------------------------------------
    # Anchor
    # --------------------------------------------------------

    anchor_hash(
        web3,
        contract,
        sha256_hex,
        source
    )

    # --------------------------------------------------------
    # Verify
    # --------------------------------------------------------

    verify_hash(
        web3,
        contract,
        sha256_hex
    )