// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EventLogger {
    event EventLogged(string hash, string details, uint256 timestamp);

    function logEvent(string memory _hash, string memory _details) public {
        emit EventLogged(_hash, _details, block.timestamp);
    }
}
