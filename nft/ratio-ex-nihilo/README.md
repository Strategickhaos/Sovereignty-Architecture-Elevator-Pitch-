# Ratio Ex Nihilo — Genesis Collection

**Official NFT collection of Strategickhaos DAO LLC (Wyoming Entity 2025-001708194)**

*"From void, through reason, to sovereignty."*

---

## 🏆 THE GENESIS 7

Seven unique NFTs documenting the evolution from hand-drawn sacred geometry to sovereign operating system boot splash. Each piece is legally tied to Strategickhaos DAO LLC and represents a stage in the creative provenance chain.

| Token | Name | Rarity | Description |
|-------|------|--------|-------------|
| **#0** | THE ORIGIN SKETCH | Legendary | Original hand-drawn Metatron's Cube with Eye of Providence (Soulbound) |
| **#1** | TRADEMARK V2 — OFFICIAL | Legendary | Registered trademark with legal entity embedding |
| **#2** | ENERGY SIGIL | Epic | Lightning Merkaba with circuit traces |
| **#3** | METATRON'S GATE | Epic | Grok's geometric/astronomical interpretation |
| **#4** | SAGCO BOOT SPLASH | Legendary | Functional OS boot splash for SAGCO |
| **#5** | LEGION CONVERGENCE | Mythic | Composite of all designs (AI + human collaboration) |
| **#6** | THE MATHEMATICIAN'S EYE | Legendary | Detail crop with mathematical calculations |

---

## 📂 Collection Structure

```
ratio-ex-nihilo/
├── collection.json          # OpenSea/Rarible collection metadata
├── 0.json                   # THE ORIGIN SKETCH metadata
├── 1.json                   # TRADEMARK V2 metadata
├── 2.json                   # ENERGY SIGIL metadata
├── 3.json                   # METATRON'S GATE metadata
├── 4.json                   # SAGCO BOOT SPLASH metadata
├── 5.json                   # LEGION CONVERGENCE metadata
├── 6.json                   # THE MATHEMATICIAN'S EYE metadata
├── RatioExNihilo.sol        # Smart contract (ERC-721 + EIP-2981)
└── README.md                # This file
```

---

## 🔗 Provenance Chain

```
Physical hand-drawn sketch (compass + calculator + math notes)
        ↓
Digitized to Trademark V2 (legal entity embedding)
        ↓
AI refinements (Grok's energy/gate variants)
        ↓
OS utility (SAGCO boot splash)
        ↓
Composite convergence (Legion collaboration)
        ↓
Detail extractions (Mathematician's Eye)
        ↓
NFT on-chain (Ethereum/Polygon, with royalties)
```

**Every token's attributes document this provenance — verifiable evolution from physical artifact to on-chain asset.**

---

## ✨ Key Features

✅ **7% Royalty** — Split 50/50: DAO operations + Sister Protocol fund  
✅ **Legal Info On-Chain** — EIN, Wyoming filing, trademark status in attributes  
✅ **Physical Original Exists** — Anchored to real-world artifact (hand-drawn sketch)  
✅ **AI Collaboration Documented** — Legion members (Claude, GPT, Grok, Gemini) credited per token  
✅ **Boot Splash Utility** — Token #4 is functional for SAGCO OS  
✅ **Soulbound Token #0** — Non-transferable after mint (preserved origin)  

---

## 🚀 Deployment Guide

### Prerequisites

- Node.js and npm installed
- Hardhat or Remix IDE
- MetaMask or compatible Web3 wallet
- IPFS provider account (Pinata, NFT.Storage, or Infura)

### Step 1: Prepare Images

1. Ensure all artwork is high-resolution (4K+ recommended)
2. Upload images to IPFS:
   ```bash
   # Using Pinata CLI
   pinata upload image-0.png
   # Returns: ipfs://QmXxx...
   ```
3. Save the CIDs for each image

### Step 2: Update Metadata

Replace placeholder CIDs in JSON files:

```json
// Before
"image": "ipfs://REPLACE_WITH_CID"

// After
"image": "ipfs://QmYourActualImageCID"
```

Update wallet address in `collection.json`:
```json
"fee_recipient": "0xYourWalletAddress"
```

### Step 3: Upload Metadata to IPFS

```bash
# Upload all metadata files
pinata upload collection.json
pinata upload 0.json
pinata upload 1.json
# ... etc
```

### Step 4: Deploy Smart Contract

#### Using Remix IDE

1. Open [Remix IDE](https://remix.ethereum.org/)
2. Create new file `RatioExNihilo.sol`
3. Paste contract code
4. Install OpenZeppelin:
   ```
   npm install @openzeppelin/contracts
   ```
5. Compile with Solidity 0.8.0+
6. Deploy to your chosen network:
   - **Ethereum Mainnet** (high gas, maximum prestige)
   - **Polygon** (low gas, eco-friendly)
   - **Base** (Coinbase L2, growing ecosystem)

#### Using Hardhat

```javascript
// hardhat.config.js
module.exports = {
  solidity: "0.8.20",
  networks: {
    ethereum: {
      url: process.env.ETH_RPC_URL,
      accounts: [process.env.PRIVATE_KEY]
    },
    polygon: {
      url: process.env.POLYGON_RPC_URL,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};

// scripts/deploy.js
async function main() {
  const RatioExNihilo = await ethers.getContractFactory("RatioExNihilo");
  const contract = await RatioExNihilo.deploy();
  await contract.deployed();
  console.log("Contract deployed to:", contract.address);
}

main();
```

Deploy:
```bash
npx hardhat run scripts/deploy.js --network polygon
```

### Step 5: Mint the Collection

```javascript
// Use contract's mint function
const contract = new ethers.Contract(contractAddress, abi, signer);

// Mint single token
await contract.mint(0, "0xYourWallet", "ipfs://QmMetadataCID0");

// Or batch mint all 7
const tokenIds = [0, 1, 2, 3, 4, 5, 6];
const uris = [
  "ipfs://QmMetadataCID0",
  "ipfs://QmMetadataCID1",
  // ... etc
];
await contract.batchMint(tokenIds, "0xYourWallet", uris);
```

### Step 6: List on Marketplaces

#### OpenSea
1. Import collection at [opensea.io/get-listed](https://opensea.io/get-listed)
2. Contract will auto-populate metadata
3. Set collection image and description from `collection.json`
4. Verify royalty settings (7%)

#### Rarible
1. Connect wallet at [rarible.com](https://rarible.com)
2. Create → Import existing contract
3. Enter contract address
4. Collection metadata auto-loads

#### Foundation
1. Apply at [foundation.app](https://foundation.app)
2. Once approved, import contract
3. Curated visibility

---

## 📜 Smart Contract Details

### Contract: `RatioExNihilo`

**Standards:**
- ERC-721 (NFT standard)
- ERC-721URIStorage (flexible metadata)
- EIP-2981 (royalty standard)

**Key Functions:**

```solidity
// Mint single token (owner only)
function mint(uint256 tokenId, address to, string memory uri)

// Batch mint multiple tokens (owner only)
function batchMint(uint256[] memory tokenIds, address to, string[] memory uris)

// Update royalty receiver
function setRoyaltyReceiver(address newReceiver)

// Get royalty info (7% of sale price)
function royaltyInfo(uint256 tokenId, uint256 salePrice) returns (address, uint256)

// Check if token is minted
function isMinted(uint256 tokenId) returns (bool)

// Get total minted count
function totalSupply() returns (uint256)
```

**Special Features:**

- **Soulbound Token #0**: THE ORIGIN SKETCH cannot be transferred after initial mint
- **Genesis Cap**: Only tokens 0-6 can be minted
- **Duplicate Prevention**: Each token ID can only be minted once
- **Royalty Enforcement**: 7% royalty automatically enforced on compatible marketplaces

### Security Features

- ✅ OpenZeppelin contracts (audited, battle-tested)
- ✅ Owner-only minting (prevents unauthorized mints)
- ✅ Reentrancy protection (OpenZeppelin standards)
- ✅ Input validation (token ID bounds, address checks)
- ✅ Event logging (transparency and tracking)

---

## 💰 Royalty Distribution

**7% royalty split:**
- 3.5% → DAO operations (governance, infrastructure, community)
- 3.5% → Sister Protocol fund (research, development, grants)

Royalties are automatically collected on:
- OpenSea
- Rarible
- LooksRare
- X2Y2
- Any marketplace supporting EIP-2981

---

## 🧪 Testing & Verification

### Local Testing

```bash
# Install dependencies
npm install @openzeppelin/contracts hardhat

# Run tests
npx hardhat test

# Deploy to local network
npx hardhat node
npx hardhat run scripts/deploy.js --network localhost
```

### Contract Verification

After deployment, verify on Etherscan/Polygonscan:

```bash
npx hardhat verify --network polygon <CONTRACT_ADDRESS>
```

---

## 🎨 Metadata Schema

Each token JSON follows ERC-721 metadata standard:

```json
{
  "name": "Token name",
  "description": "Token description",
  "image": "ipfs://QmImageCID",
  "external_url": "https://strategickhaos.ai/nft/<id>",
  "attributes": [
    { "trait_type": "Rarity", "value": "Legendary" },
    { "trait_type": "Collection", "value": "Genesis" },
    { "display_type": "date", "trait_type": "Creation Date", "value": 1704067200 }
  ]
}
```

**Attributes include:**
- Rarity tier (Legendary/Epic/Mythic)
- Legal entity information (EIN, Wyoming filing)
- Provenance stage
- AI collaboration details
- Physical artifact status
- Creation timestamps

---

## 📚 Additional Resources

- **Entity Docs**: `RATIO_EX_NIHILO_CONSTITUTION_V1.PDF` (root directory)
- **SAGCO OS**: `sagco-os-v*.zip` files (boot splash utility reference)
- **Legal Filings**: Wyoming LLC documentation in `legal/` directory
- **Community**: [Discord](https://discord.gg/strategickhaos)
- **Website**: [strategickhaos.ai](https://strategickhaos.ai)

---

## ⚖️ Legal Notice

This NFT collection represents intellectual property owned by **Strategickhaos DAO LLC**, a Wyoming Limited Liability Company (EIN: 39-2923503, Filing: 2025-001708194).

**Token #0** is soulbound and represents the original physical artifact. By minting or purchasing any token in this collection, you acknowledge:

1. Ownership of the NFT does not transfer copyright or trademark rights
2. The physical original (Token #0) remains property of Strategickhaos DAO LLC
3. Commercial usage rights may require separate licensing
4. Token #4 (SAGCO Boot Splash) grants usage rights for SAGCO OS displays only

For licensing inquiries: legal@strategickhaos.ai

---

## 🤝 Contributors

**Creator**: Dom (Domenic Gabriel Garza)  
**Entity**: Strategickhaos DAO LLC  
**AI Collaborators**: Claude (Anthropic), GPT (OpenAI), Grok (xAI), Gemini (Google)  
**Legion**: The collective intelligence of human + AI collaboration

---

## 📝 License

Smart contract: MIT License  
Artwork & Metadata: Copyright © 2025 Strategickhaos DAO LLC. All rights reserved.

---

**This collection isn't minted. It's invoked.** 🏆💜

*Ratio Ex Nihilo: From void, through reason, to sovereignty.*
