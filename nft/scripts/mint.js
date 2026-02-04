// Minting script for Ratio Ex Nihilo Genesis Collection
// Mints all 7 NFTs with proper metadata URIs

const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

// Token metadata URIs (update these with actual IPFS CIDs after upload)
const METADATA_BASE_URI = process.env.IPFS_BASE_URI || "ipfs://[BASE_CID]/";

const GENESIS_TOKENS = [
  {
    id: 0,
    name: "The Origin Sketch",
    uri: `${METADATA_BASE_URI}token_0.json`,
    soulbound: true,
    recipient: process.env.CREATOR_ADDRESS // Should be creator's address for soulbound token
  },
  {
    id: 1,
    name: "Trademark V2",
    uri: `${METADATA_BASE_URI}token_1.json`,
    soulbound: false,
    recipient: process.env.TREASURY_ADDRESS
  },
  {
    id: 2,
    name: "Energy Sigil",
    uri: `${METADATA_BASE_URI}token_2.json`,
    soulbound: false,
    recipient: process.env.TREASURY_ADDRESS
  },
  {
    id: 3,
    name: "Metatron's Gate",
    uri: `${METADATA_BASE_URI}token_3.json`,
    soulbound: false,
    recipient: process.env.TREASURY_ADDRESS
  },
  {
    id: 4,
    name: "SAGCO Boot Splash",
    uri: `${METADATA_BASE_URI}token_4.json`,
    soulbound: false,
    recipient: process.env.TREASURY_ADDRESS
  },
  {
    id: 5,
    name: "Legion Convergence",
    uri: `${METADATA_BASE_URI}token_5.json`,
    soulbound: false,
    recipient: process.env.TREASURY_ADDRESS
  },
  {
    id: 6,
    name: "The Mathematician's Eye",
    uri: `${METADATA_BASE_URI}token_6.json`,
    soulbound: false,
    recipient: process.env.TREASURY_ADDRESS
  }
];

async function main() {
  console.log("🔥 Minting Ratio Ex Nihilo Genesis Collection...\n");

  // Get contract address from environment or command line
  const CONTRACT_ADDRESS = process.env.CONTRACT_ADDRESS || process.argv[2];
  
  if (!CONTRACT_ADDRESS) {
    console.error("❌ Error: Contract address not provided");
    console.error("Usage: npx hardhat run scripts/mint.js --network <network> <contract_address>");
    console.error("   or: Set CONTRACT_ADDRESS environment variable");
    process.exit(1);
  }

  // Get the deployer/minter account
  const [minter] = await hre.ethers.getSigners();
  console.log("Minting from account:", minter.address);
  console.log("Contract address:", CONTRACT_ADDRESS);

  // Attach to deployed contract
  const RatioExNihilo = await hre.ethers.getContractFactory("RatioExNihilo");
  const ratioExNihilo = RatioExNihilo.attach(CONTRACT_ADDRESS);

  // Verify contract is accessible
  try {
    const name = await ratioExNihilo.name();
    console.log("Contract name:", name);
  } catch (error) {
    console.error("❌ Error: Cannot connect to contract at", CONTRACT_ADDRESS);
    console.error(error.message);
    process.exit(1);
  }

  // Check current supply
  const currentSupply = await ratioExNihilo.totalMinted();
  console.log("\nCurrent supply:", currentSupply.toString());

  if (currentSupply >= 7) {
    console.log("✅ All tokens already minted!");
    process.exit(0);
  }

  // Mint each token
  console.log("\n🎨 Minting Genesis Collection...\n");
  
  for (const token of GENESIS_TOKENS) {
    const recipient = token.recipient || minter.address;
    
    console.log(`Minting Token #${token.id}: ${token.name}`);
    console.log(`  Recipient: ${recipient}`);
    console.log(`  Soulbound: ${token.soulbound}`);
    console.log(`  URI: ${token.uri}`);

    try {
      const tx = await ratioExNihilo.mint(recipient, token.uri, token.soulbound);
      console.log(`  Transaction: ${tx.hash}`);
      
      const receipt = await tx.wait();
      console.log(`  ✅ Minted in block ${receipt.blockNumber}`);
      
      // Verify soulbound status
      if (token.soulbound) {
        const isSoulbound = await ratioExNihilo.isSoulbound(token.id);
        console.log(`  🔒 Soulbound status verified: ${isSoulbound}`);
      }
      
      console.log();
    } catch (error) {
      console.error(`  ❌ Error minting token #${token.id}:`, error.message);
      if (error.message.includes("Max supply reached")) {
        console.log("  ℹ️  This token may have already been minted");
      }
    }
  }

  // Display final status
  const finalSupply = await ratioExNihilo.totalMinted();
  console.log("\n📊 Final Status:");
  console.log(`  Total Minted: ${finalSupply} / 7`);
  console.log(`  Remaining: ${7 - finalSupply}`);

  if (finalSupply >= 7) {
    console.log("\n🎉 Genesis Collection Minting Complete!");
    console.log("\n📝 Next Steps:");
    console.log("1. Verify all tokens appear correctly");
    console.log("2. Test royalty functionality");
    console.log("3. List collection on OpenSea");
    console.log("4. Announce launch on Discord/Twitter");
    console.log("\n🔥💜 RATIO EX NIHILO 💜🔥");
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
