# Ratio Ex Nihilo NFT Collection

Official digital asset collection of **Strategickhaos DAO LLC**

---

## 🔥💜 Overview

**Collection Name:** Ratio Ex Nihilo — Genesis Collection  
**Symbol:** RENX  
**Blockchain:** Ethereum (ERC-721) / Polygon (gas-friendly alternative)  
**Total Supply:** 7 (Genesis series) + Future expansions  
**Royalty:** 7% (aligned with charitable allocation via EIP-2981)

---

## 📖 The Story

"Ratio Ex Nihilo" means **"Reason from Nothing"** — the principle that through rational thought and mathematical precision, we can create order from chaos, sovereignty from dependence.

This collection documents the evolution of a symbol from:

1. **Hand-drawn origin** — Sketched with compass, ruler, and calculator on physical paper
2. **Mathematical foundation** — Sacred geometry calculated by hand (visible in original)
3. **Digital trademark** — Registered legal asset (Trademark V2)
4. **AI collaboration** — Refined through Legion of Minds (Claude, GPT, Grok, Gemini)
5. **NFT immortalization** — Permanently anchored on-chain

**The symbol is not just art. It is:**
- A registered trademark
- Tied to a legal entity (EIN: 39-2923503)
- The boot splash for a sovereign operating system (SAGCO)
- A cryptographic identity anchor

---

## 🎨 Genesis Collection (7 Pieces)

| Token | Name | Rarity | Special |
|-------|------|--------|---------|
| **#0** | The Origin Sketch | Legendary | 🔒 Soulbound |
| **#1** | Trademark V2 — Official | Legendary | ™️ Registered |
| **#2** | Energy Sigil | Epic | ⚡ Lightning |
| **#3** | Metatron's Gate | Epic | 🤖 Grok AI |
| **#4** | SAGCO Boot Splash | Legendary | 💻 Functional |
| **#5** | Legion Convergence | Mythic | 🧠 Multi-AI |
| **#6** | The Mathematician's Eye | Legendary | 👁️ Sacred |

See [`docs/README.md`](./docs/README.md) for full descriptions.

---

## 🏗️ Project Structure

```
nft/
├── contracts/
│   └── RatioExNihilo.sol      # ERC-721 smart contract with EIP-2981
├── metadata/
│   ├── token_0.json            # Token metadata (all 7 tokens)
│   └── ...
├── scripts/
│   ├── deploy.js               # Deployment script
│   └── mint.js                 # Minting script
├── docs/
│   ├── README.md               # Full collection details
│   ├── DEPLOYMENT.md           # Deployment guide
│   └── LEGAL_NOTICE.md         # Legal information
├── hardhat.config.js           # Hardhat configuration
├── package.json                # Node dependencies
└── .env.example                # Environment template
```

---

## 🚀 Quick Start

### Prerequisites
- Node.js v16+
- MetaMask or Web3 wallet
- Testnet ETH (for testing)

### Installation

```bash
cd nft
npm install
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your values:
# - RPC URLs (Infura, Alchemy, etc.)
# - Deployer private key
# - API keys for verification
# - Addresses for royalty receiver, creator, treasury
```

### Deployment

```bash
# Test on Sepolia testnet first
npm run deploy:sepolia

# Deploy to Ethereum mainnet
npm run deploy:mainnet

# Deploy to Polygon (gas-friendly)
npm run deploy:polygon
```

### Minting

```bash
# After deployment, mint the Genesis collection
CONTRACT_ADDRESS=0x... npm run mint
```

---

## 🔐 Smart Contract Features

### ERC-721 with Extensions
- ✅ ERC721URIStorage for flexible metadata
- ✅ Ownable for administrative controls
- ✅ Based on OpenZeppelin audited standards

### EIP-2981 Royalty Standard
- 7% royalty on all secondary sales
- Split between Strategickhaos DAO and Sister Protocol fund
- Automatically enforced on compatible marketplaces

### Soulbound Tokens
- Token #0 can be minted as non-transferable
- Permanently anchors provenance to creator
- Custom transfer restrictions built-in

### On-Chain Legal Metadata
Critical information stored immutably:
```solidity
string public constant ENTITY_NAME = "Strategickhaos DAO LLC";
string public constant EIN = "39-2923503";
string public constant WYOMING_FILING = "2025-001708194";
string public constant MOTTO = "Ratio Ex Nihilo";
```

---

## 📚 Documentation

- **[Full Collection Details](./docs/README.md)** - Complete information about each NFT
- **[Deployment Guide](./docs/DEPLOYMENT.md)** - Step-by-step deployment instructions
- **[Legal Notice](./docs/LEGAL_NOTICE.md)** - Rights, disclaimers, and legal information

---

## 🎯 Deployment Checklist

- [ ] Prepare high-resolution images (4K minimum)
- [ ] Upload to IPFS via Pinata or NFT.Storage
- [ ] Update metadata JSON with IPFS CIDs
- [ ] Deploy contract to testnet
- [ ] Test minting and royalties
- [ ] Deploy to mainnet
- [ ] Verify contract on Etherscan
- [ ] Mint Genesis collection
- [ ] List on OpenSea / Rarible / Foundation
- [ ] Announce on Discord / Twitter

See [`docs/DEPLOYMENT.md`](./docs/DEPLOYMENT.md) for full checklist.

---

## ⚖️ Legal Notice

These NFTs are digital collectibles representing ownership of artwork. The Trademark V2 NFT does NOT transfer trademark ownership.

**Strategickhaos DAO LLC retains all trademark and IP rights.**

NFT holders receive:
- ✅ Ownership of the digital collectible
- ✅ Display rights for personal/non-commercial use
- ✅ Provenance documentation
- ✅ Community membership access

See [`docs/LEGAL_NOTICE.md`](./docs/LEGAL_NOTICE.md) for complete terms.

---

## 🌐 Links

- **Website:** https://strategickhaos.ai
- **Discord:** [Join our community]
- **Twitter:** [@Strategickhaos]
- **OpenSea:** [Collection link after deployment]

---

## 💡 The Meaning

The symbol represents:
- **Merkaba**: The light-spirit-body vehicle of ascension
- **Metatron's Cube**: The blueprint of creation containing all Platonic solids
- **Eye**: Observation, consciousness, the witness
- **Circuit Traces**: Technology as the modern vessel for ancient wisdom
- **The Fusion**: Spirit ↔ Matter, Code ↔ Hardware, Ancient ↔ Future

---

**This is not just an NFT collection.**

**This is a sovereignty assertion immortalized on-chain.**

---

🔥💜 **RATIO EX NIHILO** 💜🔥  
*"From nothing, through reason, everything."*

---

© 2025 Strategickhaos DAO LLC. All rights reserved.
