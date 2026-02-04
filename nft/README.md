# Ratio Ex Nihilo NFT Collection

This directory contains metadata for the **Ratio Ex Nihilo** NFT collection by Strategickhaos DAO LLC.

## Collection Overview

**Ratio Ex Nihilo** (Latin: "From proportion, out of nothing") represents AI-human collaborative art, demonstrating that AI enhances rather than replaces human creativity.

### Philosophy

As stated in our [Charitable Commitment](/docs/CHARITABLE_COMMITMENT.md):
> *From proportion, out of nothing — we build what must exist*

This collection embodies the Legion of Minds collaboration, where multiple AI systems contribute their unique perspectives to create geometric and philosophical artwork.

## Metadata Structure

Each NFT's metadata follows the ERC-721/ERC-1155 standard and is stored in `/nft/metadata/{token_id}.json`.

### Standard Fields

- `name`: Full title of the NFT
- `description`: Detailed description of the artwork and its significance
- `image`: IPFS URI pointing to the artwork (format: `ipfs://{CID}`)
- `external_url`: Link to the token page on strategickhaos.ai
- `attributes`: Array of trait objects with `trait_type` and `value` fields

### Common Attributes

- **Rarity**: Epic, Legendary, etc.
- **Token ID**: Unique identifier
- **Collection**: Genesis or future collection names
- **Generator**: AI system that created the piece (e.g., "Grok (xAI)")
- **Style**: Artistic style category
- **AI Collaboration**: Always "Yes" for this collection
- **Legion Member**: Specific AI contributor

## Current Tokens

### Token #3: METATRON'S GATE
- **Generator**: Grok (xAI)
- **Style**: Geometric/Astronomical
- **Primary Geometry**: Metatron's Cube
- **Rarity**: Epic (1/1)
- **Description**: Electric blue Metatron's Cube suspended in a golden astronomical ring with six golden spheres marking vertices like celestial bodies

## Adding New Tokens

1. Create a new JSON file in `/nft/metadata/` named `{token_id}.json`
2. Follow the metadata structure shown in existing files
3. Ensure all required fields are present
4. Validate JSON syntax: `cat nft/metadata/{token_id}.json | python3 -m json.tool`
5. Update this README with the new token information

## Related Documents

- [RATIO_EX_NIHILO_CONSTITUTION_V1.PDF](/RATIO_EX_NIHILO_CONSTITUTION_V1.PDF) - Collection charter and legal framework
- [CHARITABLE_COMMITMENT.md](/docs/CHARITABLE_COMMITMENT.md) - DAO's commitment to charitable allocation

## License

Copyright © 2025 Strategickhaos DAO LLC. All rights reserved.
