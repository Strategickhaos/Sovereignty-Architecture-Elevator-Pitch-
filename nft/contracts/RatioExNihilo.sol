// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/interfaces/IERC2981.sol";

/**
 * @title RatioExNihilo
 * @dev ERC-721 NFT contract for the Ratio Ex Nihilo Genesis Collection
 * Official digital asset collection of Strategickhaos DAO LLC
 * 
 * Collection: Genesis (7 pieces)
 * Symbol: RENX
 * Entity: Strategickhaos DAO LLC (EIN: 39-2923503, Wyoming Filing: 2025-001708194)
 */
contract RatioExNihilo is ERC721, ERC721URIStorage, Ownable, IERC2981 {
    // Collection constants
    uint256 public constant MAX_SUPPLY = 7;
    uint256 public constant ROYALTY_BASIS_POINTS = 700; // 7%
    
    // State variables
    uint256 private _tokenIdCounter;
    address private _royaltyReceiver;
    
    // On-chain legal metadata
    string public constant ENTITY_NAME = "Strategickhaos DAO LLC";
    string public constant EIN = "39-2923503";
    string public constant WYOMING_FILING = "2025-001708194";
    string public constant MOTTO = "Ratio Ex Nihilo";
    
    // Soulbound tokens (non-transferable)
    mapping(uint256 => bool) private _soulbound;
    
    // Events
    event TokenMinted(uint256 indexed tokenId, address indexed recipient, string tokenURI);
    event RoyaltyReceiverUpdated(address indexed oldReceiver, address indexed newReceiver);
    event TokenSoulbound(uint256 indexed tokenId);
    
    /**
     * @dev Constructor
     * @param royaltyReceiver Address to receive royalties
     */
    constructor(address royaltyReceiver) ERC721("Ratio Ex Nihilo", "RENX") Ownable(msg.sender) {
        require(royaltyReceiver != address(0), "Invalid royalty receiver");
        _royaltyReceiver = royaltyReceiver;
    }
    
    /**
     * @dev Mint a new NFT
     * @param recipient Address to receive the NFT
     * @param tokenURI Metadata URI for the NFT
     * @param soulbound Whether this token should be non-transferable
     */
    function mint(address recipient, string memory tokenURI, bool soulbound) external onlyOwner {
        require(_tokenIdCounter < MAX_SUPPLY, "Max supply reached");
        require(recipient != address(0), "Invalid recipient");
        
        uint256 tokenId = _tokenIdCounter;
        _tokenIdCounter++;
        
        _safeMint(recipient, tokenId);
        _setTokenURI(tokenId, tokenURI);
        
        if (soulbound) {
            _soulbound[tokenId] = true;
            emit TokenSoulbound(tokenId);
        }
        
        emit TokenMinted(tokenId, recipient, tokenURI);
    }
    
    /**
     * @dev Check if a token is soulbound
     * @param tokenId Token ID to check
     */
    function isSoulbound(uint256 tokenId) public view returns (bool) {
        return _soulbound[tokenId];
    }
    
    /**
     * @dev Override transfer functions to prevent soulbound transfers
     */
    function _update(address to, uint256 tokenId, address auth) internal virtual override returns (address) {
        address from = _ownerOf(tokenId);
        
        // Allow minting (from == address(0)) but prevent transfers of soulbound tokens
        if (from != address(0) && _soulbound[tokenId]) {
            revert("Token is soulbound and cannot be transferred");
        }
        
        return super._update(to, tokenId, auth);
    }
    
    /**
     * @dev EIP-2981 royalty info
     * Returns royalty receiver and amount for a given sale price
     */
    function royaltyInfo(uint256 /* tokenId */, uint256 salePrice) 
        external 
        view 
        override 
        returns (address receiver, uint256 royaltyAmount) 
    {
        uint256 royalty = (salePrice * ROYALTY_BASIS_POINTS) / 10000;
        return (_royaltyReceiver, royalty);
    }
    
    /**
     * @dev Update royalty receiver
     * @param newReceiver New royalty receiver address
     */
    function updateRoyaltyReceiver(address newReceiver) external onlyOwner {
        require(newReceiver != address(0), "Invalid receiver");
        address oldReceiver = _royaltyReceiver;
        _royaltyReceiver = newReceiver;
        emit RoyaltyReceiverUpdated(oldReceiver, newReceiver);
    }
    
    /**
     * @dev Get current royalty receiver
     */
    function getRoyaltyReceiver() external view returns (address) {
        return _royaltyReceiver;
    }
    
    /**
     * @dev Get total number of minted tokens
     */
    function totalMinted() external view returns (uint256) {
        return _tokenIdCounter;
    }
    
    // Required overrides
    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }
    
    function supportsInterface(bytes4 interfaceId) 
        public 
        view 
        override(ERC721, ERC721URIStorage, IERC165) 
        returns (bool) 
    {
        return interfaceId == type(IERC2981).interfaceId || super.supportsInterface(interfaceId);
    }
}
