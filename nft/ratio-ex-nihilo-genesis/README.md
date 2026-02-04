# Ratio Ex Nihilo Genesis Collection

Official NFT collection of **Strategickhaos DAO LLC** (Wyoming Entity: 2025-001708194)

## Collection Overview

The **Ratio Ex Nihilo Genesis Collection** is a seven-piece NFT series documenting the evolution from hand-drawn sacred geometry to the sovereign operating system boot splash. This collection represents the foundational visual journey of the Strategickhaos sovereignty architecture.

## Legal Connection

Each piece in this collection is legally tied to:
- **Entity**: Strategickhaos DAO LLC
- **Wyoming File Number**: 2025-001708194
- **EIN**: 39-2900295

## Collection Details

- **Total Pieces**: 7
- **Royalty Fee**: 7% (700 basis points)
- **External Link**: https://strategickhaos.ai

## Files

- `collection.json` - OpenSea-compatible collection metadata
- `README.md` - This documentation file

## Setup Instructions

Before deploying this collection to a blockchain or NFT marketplace, you need to update the placeholder values in `collection.json`:

### 1. Upload Collection Cover Image to IPFS

Upload your collection cover image to IPFS and replace `COLLECTION_IMAGE_CID` with the actual CID:

```json
"image": "ipfs://YOUR_ACTUAL_CID_HERE"
```

### 2. Set Fee Recipient Wallet Address

Replace `0xYOUR_WALLET_ADDRESS` with the actual Ethereum wallet address that will receive royalties:

```json
"fee_recipient": "0xYourActualWalletAddress"
```

## Collection Metadata Schema

The `collection.json` file follows the OpenSea collection metadata standard:

- **name**: Collection name displayed on marketplaces
- **description**: Detailed description of the collection
- **image**: IPFS URI for collection cover image
- **external_link**: Link to project website
- **seller_fee_basis_points**: Royalty percentage (700 = 7%)
- **fee_recipient**: Ethereum address to receive royalties

## Seven Pieces Overview

The collection documents the evolution:

1. Hand-drawn sacred geometry foundations
2. Digital geometry refinements
3. Architectural blueprints
4. System architecture diagrams
5. Operating system core concepts
6. Boot sequence visualizations
7. Final sovereign OS boot splash

## Deployment Notes

- Ensure all images are uploaded to IPFS before minting
- Verify wallet address ownership before setting as fee_recipient
- Test metadata on testnet (e.g., Rinkeby, Goerli) before mainnet deployment
- Keep private keys secure and never commit them to the repository

## References

- [OpenSea Metadata Standards](https://docs.opensea.io/docs/metadata-standards)
- [IPFS Documentation](https://docs.ipfs.tech/)
- Wyoming DAO LLC Filing: 2025-001708194
