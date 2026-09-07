// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract IdentityAnchor {
    struct ProofRecord {
        bytes32 dataHash;
        uint256 timestamp;
        address submitter;
        string searchSource;
    }

    mapping(bytes32 => ProofRecord) private proofs;

    event ProofAnchored(bytes32 indexed dataHash, address indexed submitter, uint256 timestamp);

    function anchorProof(bytes32 _dataHash, string calldata _source) external {
        require(proofs[_dataHash].timestamp == 0, "Proof already exists on-chain.");
        
        proofs[_dataHash] = ProofRecord({
            dataHash: _dataHash,
            timestamp: block.timestamp,
            submitter: msg.sender,
            searchSource: _source
        });

        emit ProofAnchored(_dataHash, msg.sender, block.timestamp);
    }

    function verifyProof(bytes32 _dataHash) external view returns (bool isVerified, uint256 timestamp, address submitter, string memory source) {
        ProofRecord memory record = proofs[_dataHash];
        if (record.timestamp != 0) {
            return (true, record.timestamp, record.submitter, record.searchSource);
        }
        return (false, 0, address(0), "");
    }
}