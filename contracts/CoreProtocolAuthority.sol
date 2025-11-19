// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title Core Protocol Authority Certificate System
 * @dev SNH Engineering + Cyber certification on-chain
 * @notice Self-issued, verifiable authority seal for protocol governance
 */
contract CoreProtocolAuthority {
    
    // Authority information
    struct Authority {
        string name;
        string credentials;
        string orcid;
        string twic;
        bytes32 certHash;
        uint256 issuedAt;
        bool isActive;
    }
    
    // Certificate information
    struct Certificate {
        bytes32 certId;
        address holder;
        string authorityType;
        string scope;
        uint256 issuedAt;
        uint256 expiresAt;
        bool isValid;
        bytes signature;
    }
    
    // Storage
    mapping(address => Authority) public authorities;
    mapping(bytes32 => Certificate) public certificates;
    mapping(address => bytes32[]) public holderCertificates;
    
    address public immutable founderAddress;
    
    // Events
    event AuthorityRegistered(address indexed authority, string name);
    event CertificateIssued(bytes32 indexed certId, address indexed holder, string authorityType);
    event CertificateRevoked(bytes32 indexed certId);
    event AuditRequired(bytes32 indexed certId, address indexed auditor);
    
    constructor() {
        founderAddress = msg.sender;
        
        // Self-issue founder authority
        authorities[msg.sender] = Authority({
            name: "Domenic Garza - SNH Engineering + Cyber",
            credentials: "Bachelor of Science in Cybersecurity, SNHU",
            orcid: "0009-0005-2996-3526",
            twic: "Active (TSA/DHS)",
            certHash: keccak256(abi.encodePacked(msg.sender, block.timestamp)),
            issuedAt: block.timestamp,
            isActive: true
        });
        
        emit AuthorityRegistered(msg.sender, "Domenic Garza - SNH Engineering + Cyber");
    }
    
    /**
     * @notice Issue a Core Protocol Authority certificate
     * @param _holder Address receiving the certificate
     * @param _authorityType Type of authority (e.g., "Core Protocol Authority", "Audit Authority")
     * @param _scope Scope of authority
     * @param _duration Duration in seconds
     */
    function issueCertificate(
        address _holder,
        string memory _authorityType,
        string memory _scope,
        uint256 _duration
    ) external returns (bytes32) {
        require(authorities[msg.sender].isActive, "Not an active authority");
        require(_holder != address(0), "Invalid holder");
        
        bytes32 certId = keccak256(abi.encodePacked(
            _holder,
            _authorityType,
            _scope,
            block.timestamp
        ));
        
        certificates[certId] = Certificate({
            certId: certId,
            holder: _holder,
            authorityType: _authorityType,
            scope: _scope,
            issuedAt: block.timestamp,
            expiresAt: block.timestamp + _duration,
            isValid: true,
            signature: abi.encodePacked(certId)
        });
        
        holderCertificates[_holder].push(certId);
        
        emit CertificateIssued(certId, _holder, _authorityType);
        
        return certId;
    }
    
    /**
     * @notice Revoke a certificate
     * @param _certId Certificate ID to revoke
     */
    function revokeCertificate(bytes32 _certId) external {
        require(authorities[msg.sender].isActive, "Not an active authority");
        require(certificates[_certId].isValid, "Certificate not valid");
        
        certificates[_certId].isValid = false;
        
        emit CertificateRevoked(_certId);
    }
    
    /**
     * @notice Verify a certificate
     * @param _certId Certificate ID to verify
     * @return bool indicating if certificate is valid
     */
    function verifyCertificate(bytes32 _certId) external view returns (bool) {
        Certificate memory cert = certificates[_certId];
        
        return cert.isValid && 
               cert.expiresAt > block.timestamp &&
               cert.holder != address(0);
    }
    
    /**
     * @notice Trigger audit requirement for fork/deployment
     * @dev Called when someone deploys/forks the protocol
     * @param _certId Certificate ID that triggers the audit
     */
    function requireAudit(bytes32 _certId) external {
        require(certificates[_certId].isValid, "Invalid certificate");
        
        emit AuditRequired(_certId, msg.sender);
    }
    
    /**
     * @notice Get certificate details
     * @param _certId Certificate ID
     */
    function getCertificate(bytes32 _certId) external view returns (
        address holder,
        string memory authorityType,
        string memory scope,
        uint256 issuedAt,
        uint256 expiresAt,
        bool isValid
    ) {
        Certificate memory cert = certificates[_certId];
        return (
            cert.holder,
            cert.authorityType,
            cert.scope,
            cert.issuedAt,
            cert.expiresAt,
            cert.isValid
        );
    }
    
    /**
     * @notice Get all certificates for a holder
     * @param _holder Address to query
     */
    function getHolderCertificates(address _holder) external view returns (bytes32[] memory) {
        return holderCertificates[_holder];
    }
    
    /**
     * @notice Register a new authority (only by founder)
     * @param _authority Address of the new authority
     * @param _name Name of the authority
     * @param _credentials Credentials
     */
    function registerAuthority(
        address _authority,
        string memory _name,
        string memory _credentials
    ) external {
        require(msg.sender == founderAddress, "Only founder can register authorities");
        require(_authority != address(0), "Invalid authority address");
        
        authorities[_authority] = Authority({
            name: _name,
            credentials: _credentials,
            orcid: "",
            twic: "",
            certHash: keccak256(abi.encodePacked(_authority, block.timestamp)),
            issuedAt: block.timestamp,
            isActive: true
        });
        
        emit AuthorityRegistered(_authority, _name);
    }
}
