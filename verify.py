import os
import argparse
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

ETH_RPC_URL = os.getenv("ETH_RPC_URL", "http://127.0.0.1:8545")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "0x5FbDB2315678afecb367f032d93F642f64180aa3")

CONTRACT_ABI = [
    {
        "inputs": [{"internalType": "bytes32", "name": "_dataHash", "type": "bytes32"}],
        "name": "verifyProof",
        "outputs": [
            {"internalType": "bool", "name": "isVerified", "type": "bool"},
            {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
            {"internalType": "address", "name": "submitter", "type": "address"},
            {"internalType": "string", "name": "source", "type": "string"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

def verify_hash_on_chain(hex_hash: str):
    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))
    if not w3.is_connected():
        print(f"[!] Cannot connect to Web3 RPC at {ETH_RPC_URL}")
        return

    contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
    
    # Ensure bytes32 format
    bytes32_hash = bytes.fromhex(hex_hash.replace("0x", ""))
    is_verified, timestamp, submitter, source = contract.functions.verifyProof(bytes32_hash).call()

    print("\n================ ON-CHAIN VERIFICATION RESULTS ================")
    print(f" Data Hash : {hex_hash}")
    print(f" Verified  : {is_verified}")
    if is_verified:
        print(f" Timestamp : {timestamp}")
        print(f" Submitter : {submitter}")
        print(f" Source    : {source}")
    else:
        print(" [!] No matching record found on-chain.")
    print("================================================================\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hash", required=True, help="Hex string of data hash to verify")
    args = parser.parse_args()
    verify_hash_on_chain(args.hash)