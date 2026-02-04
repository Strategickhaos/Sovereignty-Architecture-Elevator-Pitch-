# Ratio Ex Nihilo NFT Collection

This directory contains the metadata for the **Ratio Ex Nihilo** NFT collection — a series documenting the creation and evolution of the Strategickhaos visual identity and sacred geometry foundation.

## Structure

```
nft/
├── metadata/
│   ├── 0.json          # Token ID 0 - THE ORIGIN SKETCH
│   └── [future tokens...]
└── README.md
```

## Metadata Format

All metadata files follow the ERC-721/OpenSea metadata standard:

- **name**: The token name
- **description**: Detailed description of the artwork
- **image**: IPFS URI to the artwork image
- **external_url**: Link to token page on strategickhaos.ai
- **attributes**: Array of trait objects with trait_type and value

## Token #0 - THE ORIGIN SKETCH

**Rarity:** Legendary (1/1)
**Medium:** Pencil and colored pencil on paper
**Created:** January 1, 2024

The genesis piece of the collection — the original hand-drawn Metatron's Cube with Eye of Providence. Created on physical paper using traditional geometric tools (compass, ruler, calculator), this artifact represents the birth of the Strategickhaos visual identity. Mathematical calculations are visible on the left margin, documenting the sacred geometric ratios that underpin the design.

The eye at the center represents consciousness observing through sacred structure — the foundational principle of the Strategickhaos philosophy.

## Collection Philosophy

**Ratio Ex Nihilo** (Latin: "Order from Chaos") documents the journey from chaotic inspiration to structured manifestation. Each piece in the collection represents a key moment in the evolution of the Strategickhaos visual language, capturing the intersection of ancient geometric wisdom and modern computational thinking.

## IPFS Deployment

Before minting, images should be uploaded to IPFS and the `REPLACE_WITH_CID` placeholder in each metadata file should be updated with the actual IPFS CID.

Example:
```json
"image": "ipfs://bafybeihx7yt34k..."
```

## Provenance

All physical originals are maintained by Strategickhaos DAO LLC and can be verified through timestamped documentation in the main repository.
