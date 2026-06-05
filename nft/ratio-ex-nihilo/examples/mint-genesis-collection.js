// Example minting script for the Genesis Collection
// Save as: scripts/mint-genesis-collection.js

const hre = require("hardhat");

async function main() {
  console.log("🎨 Minting Ratio Ex Nihilo Genesis Collection...\n");

  // Configuration - UPDATE THESE VALUES
  const CONTRACT_ADDRESS = "0xYourContractAddress"; // Replace with deployed contract
  const RECIPIENT_ADDRESS = "0xYourWalletAddress"; // Replace with your wallet

  // Metadata CIDs - UPDATE AFTER UPLOADING TO IPFS
  const metadataCIDs = [
    "ipfs://QmYourCID0", // Token #0 - THE ORIGIN SKETCH
    "ipfs://QmYourCID1", // Token #1 - TRADEMARK V2
    "ipfs://QmYourCID2", // Token #2 - ENERGY SIGIL
    "ipfs://QmYourCID3", // Token #3 - METATRON'S GATE
    "ipfs://QmYourCID4", // Token #4 - SAGCO BOOT SPLASH
    "ipfs://QmYourCID5", // Token #5 - LEGION CONVERGENCE
    "ipfs://QmYourCID6", // Token #6 - THE MATHEMATICIAN'S EYE
  ];

  // Get signer
  const [signer] = await hre.ethers.getSigners();
  console.log("📝 Minting with account:", signer.address, "\n");

  // Connect to deployed contract
  const RatioExNihilo = await hre.ethers.getContractFactory("RatioExNihilo");
  const contract = RatioExNihilo.attach(CONTRACT_ADDRESS);

  console.log("📋 Contract:", contract.address);
  console.log("👤 Recipient:", RECIPIENT_ADDRESS);
  console.log("🎫 Tokens to mint:", metadataCIDs.length, "\n");

  // Option 1: Batch mint all tokens at once (more gas efficient)
  console.log("🚀 Batch minting all tokens...\n");
  
  const tokenIds = [0, 1, 2, 3, 4, 5, 6];
  
  try {
    const tx = await contract.batchMint(tokenIds, RECIPIENT_ADDRESS, metadataCIDs);
    console.log("⏳ Transaction hash:", tx.hash);
    console.log("⏳ Waiting for confirmation...");
    
    const receipt = await tx.wait();
    console.log("✅ Batch mint successful! Block:", receipt.blockNumber, "\n");
    
    // Log each minted token
    for (let i = 0; i < tokenIds.length; i++) {
      console.log(`✅ Token #${tokenIds[i]} minted`);
      console.log(`   URI: ${metadataCIDs[i]}`);
      console.log(`   Owner: ${RECIPIENT_ADDRESS}`);
    }
  } catch (error) {
    console.error("❌ Batch mint failed:", error.message);
    console.log("\n📌 Falling back to individual minting...\n");
    
    // Option 2: Mint tokens individually (fallback if batch fails)
    for (let i = 0; i < tokenIds.length; i++) {
      try {
        console.log(`\n🎨 Minting Token #${tokenIds[i]}...`);
        
        const tx = await contract.mint(tokenIds[i], RECIPIENT_ADDRESS, metadataCIDs[i]);
        console.log("⏳ Transaction hash:", tx.hash);
        
        const receipt = await tx.wait();
        console.log(`✅ Token #${tokenIds[i]} minted! Block: ${receipt.blockNumber}`);
        console.log(`   URI: ${metadataCIDs[i]}`);
        console.log(`   Gas used: ${receipt.gasUsed.toString()}`);
      } catch (tokenError) {
        console.error(`❌ Failed to mint Token #${tokenIds[i]}:`, tokenError.message);
      }
    }
  }

  // Display final status
  console.log("\n📊 Final Collection Status:");
  const totalSupply = await contract.totalSupply();
  console.log(`   Total minted: ${totalSupply}/7`);
  
  console.log("\n🔍 Verifying tokens:");
  for (let i = 0; i <= 6; i++) {
    const isMinted = await contract.isMinted(i);
    const status = isMinted ? "✅ Minted" : "❌ Not minted";
    console.log(`   Token #${i}: ${status}`);
    
    if (isMinted) {
      try {
        const tokenURI = await contract.tokenURI(i);
        const owner = await contract.ownerOf(i);
        console.log(`      URI: ${tokenURI}`);
        console.log(`      Owner: ${owner}`);
      } catch (e) {
        console.log("      (Unable to fetch details)");
      }
    }
  }

  console.log("\n🎉 Minting process complete!");
  console.log("\n📝 Next steps:");
  console.log("1. Verify tokens on block explorer");
  console.log("2. Import to OpenSea/Rarible");
  console.log("3. Verify royalty settings (7%)");
  console.log("4. Announce to community!");
  console.log("\n⚠️  Remember: Token #0 is SOULBOUND and cannot be transferred!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
