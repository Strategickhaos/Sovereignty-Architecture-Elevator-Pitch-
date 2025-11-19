// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title Strategickhaos DAO LLC Cryptographic Trust
 * @dev Wyoming-compliant cryptographic trust protocol
 * @notice This contract implements auto-vesting of inventions and self-enforcing attribution tax
 */
contract CryptographicTrust {
    // DAO LLC information
    string public constant LEGAL_NAME = "Strategickhaos DAO LLC / Valoryield Engine";
    string public constant JURISDICTION = "Wyoming";
    string public constant FORMATION_DATE = "2025-06-25";
    
    // Trust parameters
    uint256 public constant ATTRIBUTION_TAX_BPS = 10; // 0.1% in basis points
    address public immutable treasuryAddress;
    address public immutable founderAddress;
    
    // Invention registry
    struct Invention {
        bytes32 codeHash;
        string name;
        string description;
        uint256 timestamp;
        bool autoVested;
        address inventor;
    }
    
    mapping(bytes32 => Invention) public inventions;
    mapping(address => bool) public authorizedUsers;
    mapping(address => uint256) public attributionBalance;
    
    // Events
    event InventionRegistered(bytes32 indexed codeHash, string name, address inventor);
    event AttributionTaxCollected(address indexed user, uint256 amount);
    event AuthorizationGranted(address indexed user);
    event AuthorizationRevoked(address indexed user);
    
    constructor(address _treasury, address _founder) {
        require(_treasury != address(0), "Invalid treasury address");
        require(_founder != address(0), "Invalid founder address");
        treasuryAddress = _treasury;
        founderAddress = _founder;
        authorizedUsers[_founder] = true;
    }
    
    /**
     * @notice Register a new invention with auto-vesting
     * @param _codeHash Cryptographic hash of the code
     * @param _name Name of the invention
     * @param _description Description of the invention
     */
    function registerInvention(
        bytes32 _codeHash,
        string memory _name,
        string memory _description
    ) external {
        require(authorizedUsers[msg.sender], "Not authorized");
        require(inventions[_codeHash].timestamp == 0, "Already registered");
        
        inventions[_codeHash] = Invention({
            codeHash: _codeHash,
            name: _name,
            description: _description,
            timestamp: block.timestamp,
            autoVested: true,
            inventor: msg.sender
        });
        
        emit InventionRegistered(_codeHash, _name, msg.sender);
    }
    
    /**
     * @notice Collect attribution tax from unauthorized users
     * @dev Silent, smooth, self-enforcing tax collection
     */
    function collectAttributionTax() external payable {
        require(msg.value > 0, "No tax sent");
        
        uint256 taxAmount = (msg.value * ATTRIBUTION_TAX_BPS) / 10000;
        attributionBalance[msg.sender] += taxAmount;
        
        // Transfer to treasury
        (bool success, ) = treasuryAddress.call{value: taxAmount}("");
        require(success, "Tax transfer failed");
        
        emit AttributionTaxCollected(msg.sender, taxAmount);
    }
    
    /**
     * @notice Grant authorization to use code without tax
     * @param _user Address to authorize
     */
    function grantAuthorization(address _user) external {
        require(msg.sender == founderAddress, "Only founder");
        authorizedUsers[_user] = true;
        emit AuthorizationGranted(_user);
    }
    
    /**
     * @notice Revoke authorization
     * @param _user Address to revoke
     */
    function revokeAuthorization(address _user) external {
        require(msg.sender == founderAddress, "Only founder");
        authorizedUsers[_user] = false;
        emit AuthorizationRevoked(_user);
    }
    
    /**
     * @notice Check if code hash is registered
     * @param _codeHash Hash to check
     * @return bool indicating if registered
     */
    function isRegistered(bytes32 _codeHash) external view returns (bool) {
        return inventions[_codeHash].timestamp > 0;
    }
    
    /**
     * @notice Get invention details
     * @param _codeHash Hash of the invention
     */
    function getInvention(bytes32 _codeHash) external view returns (
        string memory name,
        string memory description,
        uint256 timestamp,
        bool autoVested,
        address inventor
    ) {
        Invention memory inv = inventions[_codeHash];
        return (inv.name, inv.description, inv.timestamp, inv.autoVested, inv.inventor);
    }
}
