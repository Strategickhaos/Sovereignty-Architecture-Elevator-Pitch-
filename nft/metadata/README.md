# NFT Metadata Collection

This directory contains the metadata for the Strategickhaos DAO LLC NFT collection.

## Structure

Each NFT's metadata is stored in a JSON file named with its Token ID (e.g., `1.json`, `2.json`, etc.).

## Metadata Schema

The metadata follows the ERC-721 metadata standard with the following structure:

```json
{
  "name": "NFT Name",
  "description": "Detailed description of the NFT",
  "image": "ipfs://CID",
  "external_url": "https://strategickhaos.ai/nft/{token_id}",
  "attributes": [
    { "trait_type": "Attribute Name", "value": "Attribute Value" }
  ]
}
```

## Genesis Collection

### Token #1: Ratio Ex Nihilo — TRADEMARK V2 OFFICIAL

- **Rarity**: Legendary (1/1)
- **Legal Status**: Registered Trademark
- **Entity**: Strategickhaos DAO LLC
- **EIN**: 39-2923503
- **Wyoming Filing**: 2025-001708194
- **Motto**: Ratio Ex Nihilo
- **Node**: Orbiting Node 137
- **Primary Geometry**: Merkaba (Star Tetrahedron)
- **Symbolism**: Fusion of spirit and matter, code and hardware, ancient wisdom and modern technology

This NFT represents the official registered trademark of Strategickhaos DAO LLC, with legal identity embedded directly in the artwork.

## IPFS Storage

Before deployment, the `REPLACE_WITH_CID` placeholder in each metadata file should be replaced with the actual IPFS Content Identifier (CID) of the NFT artwork.

## Usage

These metadata files are designed to be:
1. Uploaded to IPFS
2. Referenced by smart contracts
3. Displayed by NFT marketplaces and wallets
4. Used for legal and identity verification

## Legal Notice

The legal information contained in these NFTs (EIN, Wyoming filing numbers, etc.) represents authentic registered entities and should be treated as official documentation.
