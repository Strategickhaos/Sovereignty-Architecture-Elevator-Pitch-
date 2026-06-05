// Example deployment script for Hardhat
// Save as: scripts/deploy-ratio-ex-nihilo.js

const hre = require("hardhat");

async function main() {
  console.log("🚀 Deploying Ratio Ex Nihilo Genesis Collection...\n");

  // Get deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("📝 Deploying with account:", deployer.address);
  console.log("💰 Account balance:", (await deployer.getBalance()).toString(), "\n");

  // Deploy contract
  const RatioExNihilo = await hre.ethers.getContractFactory("RatioExNihilo");
  const contract = await RatioExNihilo.deploy();
  await contract.deployed();

  console.log("✅ Contract deployed to:", contract.address);
  console.log("🏷️  Collection name:", await contract.name());
  console.log("🎫 Collection symbol:", await contract.symbol());
  console.log("👑 Owner:", await contract.owner());
  console.log("💎 Royalty receiver:", await contract.royaltyReceiver());
  console.log("📊 Royalty percentage:", (await contract.ROYALTY_PERCENT()) / 100, "%\n");

  // Wait for a few confirmations
  console.log("⏳ Waiting for confirmations...");
  await contract.deployTransaction.wait(5);
  console.log("✅ Confirmed!\n");

  // Verify contract on Etherscan/Polygonscan
  console.log("🔍 To verify on block explorer, run:");
  console.log(`npx hardhat verify --network ${hre.network.name} ${contract.address}\n`);

  // Save deployment info
  const fs = require("fs");
  const deploymentInfo = {
    network: hre.network.name,
    contractAddress: contract.address,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    txHash: contract.deployTransaction.hash,
  };

  fs.writeFileSync(
    "deployment-info.json",
    JSON.stringify(deploymentInfo, null, 2)
  );
  console.log("💾 Deployment info saved to deployment-info.json\n");

  console.log("🎉 Deployment complete! Next steps:");
  console.log("1. Upload images to IPFS");
  console.log("2. Update metadata JSON files with image CIDs");
  console.log("3. Upload metadata to IPFS");
  console.log("4. Mint tokens using mint-genesis-collection.js script");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
