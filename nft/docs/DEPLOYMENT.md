# Deployment Guide - Ratio Ex Nihilo NFT Collection

## Prerequisites

### Required Software
- Node.js v16+ and npm
- Hardhat or Truffle (smart contract development framework)
- MetaMask or similar Web3 wallet
- Ethereum/Polygon testnet ETH for deployment

### Required Accounts
- Ethereum wallet with deployment privileges
- IPFS/Pinata account for metadata hosting
- OpenSea/Rarible account for marketplace listing

## Deployment Checklist

### Phase 1: Preparation
- [ ] **Prepare high-resolution images** (4K minimum)
  - [ ] Token #0: Origin Sketch (scan or high-res photo)
  - [ ] Token #1: Trademark V2
  - [ ] Token #2: Energy Sigil
  - [ ] Token #3: Metatron's Gate
  - [ ] Token #4: SAGCO Boot Splash
  - [ ] Token #5: Legion Convergence
  - [ ] Token #6: Mathematician's Eye

### Phase 2: IPFS Upload
- [ ] **Upload images to IPFS**
  - [ ] Use Pinata.cloud or NFT.Storage
  - [ ] Pin all images permanently
  - [ ] Record all IPFS CIDs
  
- [ ] **Update metadata JSON files**
  - [ ] Replace `[CID]` placeholders with actual IPFS CIDs
  - [ ] Verify all attributes are correct
  - [ ] Upload metadata files to IPFS
  - [ ] Pin metadata files permanently

### Phase 3: Smart Contract Setup
- [ ] **Install dependencies**
  ```bash
  npm install --save-dev hardhat @openzeppelin/contracts
  npm install --save-dev @nomicfoundation/hardhat-toolbox
  ```

- [ ] **Configure Hardhat**
  - [ ] Set up network configuration (Ethereum mainnet/Polygon)
  - [ ] Add deployer wallet private key to environment
  - [ ] Configure Etherscan API key for verification

- [ ] **Set royalty receiver address**
  - [ ] Create or use existing multi-sig wallet
  - [ ] Configure 50/50 split: Strategickhaos DAO + Sister Protocol fund

### Phase 4: Testing
- [ ] **Test on testnet first** (Sepolia or Mumbai)
  - [ ] Deploy contract to testnet
  - [ ] Mint test tokens
  - [ ] Verify soulbound functionality for Token #0
  - [ ] Test royalty calculation
  - [ ] Verify metadata display on testnet marketplaces

### Phase 5: Mainnet Deployment
- [ ] **Deploy to mainnet**
  - [ ] Deploy RatioExNihilo contract
  - [ ] Record contract address
  - [ ] Verify contract on Etherscan/Polygonscan
  
- [ ] **Mint Genesis collection**
  - [ ] Mint Token #0 as soulbound to creator address
  - [ ] Mint Tokens #1-6 to treasury or designated addresses
  - [ ] Verify all tokens minted correctly

### Phase 6: Marketplace Integration
- [ ] **List on OpenSea**
  - [ ] Import collection
  - [ ] Set collection banner and description
  - [ ] Configure royalty settings
  - [ ] Verify collection appears correctly

- [ ] **List on additional marketplaces**
  - [ ] Rarible
  - [ ] Foundation (if applicable)
  - [ ] LooksRare

### Phase 7: Documentation & Announcement
- [ ] **Update on-chain metadata**
  - [ ] Verify legal information is accessible
  - [ ] Confirm EIN and Wyoming filing visible
  
- [ ] **Announce launch**
  - [ ] Discord announcement
  - [ ] Twitter/X announcement
  - [ ] Update strategickhaos.ai website
  - [ ] Document provenance in blog post

## Deployment Commands

### Install Dependencies
```bash
cd nft
npm init -y
npm install --save-dev hardhat @openzeppelin/contracts
npm install --save-dev @nomicfoundation/hardhat-toolbox
npx hardhat init
```

### Configure Hardhat
Create `hardhat.config.js`:
```javascript
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.20",
  networks: {
    mainnet: {
      url: process.env.MAINNET_RPC_URL,
      accounts: [process.env.DEPLOYER_PRIVATE_KEY]
    },
    polygon: {
      url: process.env.POLYGON_RPC_URL,
      accounts: [process.env.DEPLOYER_PRIVATE_KEY]
    },
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL,
      accounts: [process.env.DEPLOYER_PRIVATE_KEY]
    }
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY
  }
};
```

### Deploy Contract
```bash
npx hardhat run scripts/deploy.js --network sepolia  # Testnet
npx hardhat run scripts/deploy.js --network mainnet  # Mainnet
```

### Verify Contract
```bash
npx hardhat verify --network mainnet <CONTRACT_ADDRESS> <ROYALTY_RECEIVER_ADDRESS>
```

### Mint Tokens
```bash
npx hardhat run scripts/mint.js --network mainnet
```

## Security Considerations

1. **Multi-sig for Royalties**: Use a multi-sig wallet (Gnosis Safe) for royalty receiver
2. **Private Key Security**: Never commit private keys to git
3. **Contract Verification**: Always verify contracts on Etherscan
4. **Test First**: Always test on testnet before mainnet deployment
5. **Audit**: Consider a professional audit for high-value collections

## Post-Deployment Maintenance

- Monitor contract for any issues
- Update metadata if necessary (via IPFS)
- Respond to marketplace flagging or issues
- Track royalty distribution
- Maintain legal documentation

## Support & Resources

- OpenZeppelin Documentation: https://docs.openzeppelin.com/
- Hardhat Documentation: https://hardhat.org/docs
- IPFS Documentation: https://docs.ipfs.tech/
- OpenSea Developer Docs: https://docs.opensea.io/

---

For questions or issues, contact the Strategickhaos DAO team through official channels.
