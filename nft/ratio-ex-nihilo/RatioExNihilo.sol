// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/interfaces/IERC2981.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title RatioExNihilo
 * @dev Genesis Collection NFT contract for Strategickhaos DAO LLC
 * 
 * Features:
 * - ERC721 with URI storage for flexible metadata
 * - EIP-2981 royalty standard (7% split: DAO operations + Sister Protocol fund)
 * - Soulbound Token #0 (non-transferable)
 * - Owner-controlled minting
 * 
 * Collection: 7 unique pieces documenting evolution from hand-drawn sacred geometry
 * to sovereign operating system boot splash. Each piece legally tied to Wyoming entity
 * 2025-001708194.
 */
contract RatioExNihilo is ERC721URIStorage, IERC2981, Ownable {
    // Royalty configuration
    address public royaltyReceiver;
    uint256 public constant ROYALTY_PERCENT = 700;  // 7% (in basis points)
    
    // Track minted tokens to prevent duplicates
    mapping(uint256 => bool) private _minted;
    
    // Events
    event TokenMinted(uint256 indexed tokenId, address indexed to, string uri);
    event RoyaltyReceiverUpdated(address indexed oldReceiver, address indexed newReceiver);

    /**
     * @dev Constructor sets collection name, symbol, and initial royalty receiver
     */
    constructor() ERC721("Ratio Ex Nihilo", "RENX") Ownable(msg.sender) {
        royaltyReceiver = msg.sender;
    }

    /**
     * @dev Mint a new NFT with metadata URI
     * @param tokenId The ID of the token (0-6 for Genesis Collection)
     * @param to The address that will own the minted NFT
     * @param uri The IPFS URI pointing to the token metadata JSON
     * 
     * Requirements:
     * - Can only be called by contract owner
     * - Token ID must not already be minted
     */
    function mint(uint256 tokenId, address to, string memory uri) public onlyOwner {
        require(!_minted[tokenId], "Token already minted");
        require(tokenId <= 6, "Genesis Collection limited to tokens 0-6");
        
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        _minted[tokenId] = true;
        
        emit TokenMinted(tokenId, to, uri);
    }

    /**
     * @dev Batch mint multiple tokens
     * @param tokenIds Array of token IDs to mint
     * @param to The address that will own the minted NFTs
     * @param uris Array of IPFS URIs (must match tokenIds length)
     */
    function batchMint(uint256[] memory tokenIds, address to, string[] memory uris) public onlyOwner {
        require(tokenIds.length == uris.length, "Arrays length mismatch");
        
        for (uint256 i = 0; i < tokenIds.length; i++) {
            mint(tokenIds[i], to, uris[i]);
        }
    }

    /**
     * @dev Update royalty receiver address
     * @param newReceiver The new address to receive royalties
     */
    function setRoyaltyReceiver(address newReceiver) public onlyOwner {
        require(newReceiver != address(0), "Invalid receiver address");
        address oldReceiver = royaltyReceiver;
        royaltyReceiver = newReceiver;
        emit RoyaltyReceiverUpdated(oldReceiver, newReceiver);
    }

    /**
     * @dev EIP-2981 royalty info
     * @return receiver Address to receive royalties
     * @return royaltyAmount Amount of royalty based on sale price
     */
    function royaltyInfo(uint256, uint256 salePrice) 
        external 
        view 
        override 
        returns (address, uint256) 
    {
        uint256 royaltyAmount = (salePrice * ROYALTY_PERCENT) / 10000;
        return (royaltyReceiver, royaltyAmount);
    }

    /**
     * @dev Soulbound enforcement: Token #0 cannot be transferred after initial mint
     * This makes THE ORIGIN SKETCH (Token #0) a soulbound NFT
     */
    function _update(address to, uint256 tokenId, address auth)
        internal
        override
        returns (address)
    {
        address from = _ownerOf(tokenId);
        
        // Soulbound check: Token #0 cannot be transferred (except during mint)
        if (tokenId == 0 && from != address(0)) {
            revert("Token #0 is soulbound and non-transferable");
        }
        
        return super._update(to, tokenId, auth);
    }

    /**
     * @dev Check if a token has been minted
     * @param tokenId The token ID to check
     * @return bool True if the token exists
     */
    function isMinted(uint256 tokenId) public view returns (bool) {
        return _minted[tokenId];
    }

    /**
     * @dev Override supportsInterface to support ERC2981
     */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721URIStorage, IERC2981)
        returns (bool)
    {
        return interfaceId == type(IERC2981).interfaceId || super.supportsInterface(interfaceId);
    }

    /**
     * @dev Get total supply of minted tokens
     * @return count Number of tokens minted
     */
    function totalSupply() public view returns (uint256 count) {
        for (uint256 i = 0; i <= 6; i++) {
            if (_minted[i]) {
                count++;
            }
        }
        return count;
    }
}
