// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title SovereignNode
 * @notice Cryptographic declaration of symbolic participation in the
 *         Unified Geometric Intelligence network.
 *         Each address may register a geometry hash representing their
 *         unique symbolic identity.
 */
contract SovereignNode {

    struct Node {
        string  geometryHash;   // SHA-256 of user's symbolic geometry
        uint256 timestamp;
        bool    active;
    }

    mapping(address => Node) public nodes;

    event NodeDeclared(address indexed sovereign, string geometryHash, uint256 timestamp);
    event NodeRevoked (address indexed sovereign, uint256 timestamp);

    /// @notice Register your sovereign geometry hash on-chain.
    function declareNode(string calldata _geometryHash) external {
        require(bytes(_geometryHash).length > 0, "Geometry hash required");
        require(!nodes[msg.sender].active,        "Node already active");
        nodes[msg.sender] = Node({
            geometryHash: _geometryHash,
            timestamp:    block.timestamp,
            active:       true
        });
        emit NodeDeclared(msg.sender, _geometryHash, block.timestamp);
    }

    /// @notice Revoke your node (optional).
    function revokeNode() external {
        require(nodes[msg.sender].active, "No active node");
        nodes[msg.sender].active = false;
        emit NodeRevoked(msg.sender, block.timestamp);
    }

    /// @notice Read your own node.
    function getMyNode() external view returns (Node memory) {
        return nodes[msg.sender];
    }
}
