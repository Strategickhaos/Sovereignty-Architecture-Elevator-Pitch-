// Deployment script for Ratio Ex Nihilo NFT Collection
// Deploy the RatioExNihilo ERC-721 contract with royalty support

const hre = require("hardhat");

async function main() {
  console.log("🔥 Deploying Ratio Ex Nihilo NFT Collection...\n");

  // Get the deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying from account:", deployer.address);
  console.log("Account balance:", (await hre.ethers.provider.getBalance(deployer.address)).toString());

  // Set the royalty receiver address
  // IMPORTANT: Replace with actual multi-sig wallet address before mainnet deployment
  const ROYALTY_RECEIVER = process.env.ROYALTY_RECEIVER_ADDRESS || deployer.address;
  
  if (ROYALTY_RECEIVER === deployer.address) {
    console.warn("\n⚠️  WARNING: Using deployer address as royalty receiver.");
    console.warn("⚠️  For production, use a multi-sig wallet!\n");
  }

  console.log("Royalty receiver:", ROYALTY_RECEIVER);
  console.log("\nDeploying contract...");

  // Deploy the contract
  const RatioExNihilo = await hre.ethers.getContractFactory("RatioExNihilo");
  const ratioExNihilo = await RatioExNihilo.deploy(ROYALTY_RECEIVER);

  await ratioExNihilo.waitForDeployment();
  const contractAddress = await ratioExNihilo.getAddress();

  console.log("\n✅ RatioExNihilo deployed to:", contractAddress);
  console.log("\n📋 Contract Details:");
  console.log("   Name:", await ratioExNihilo.name());
  console.log("   Symbol:", await ratioExNihilo.symbol());
  console.log("   Max Supply:", await ratioExNihilo.MAX_SUPPLY());
  console.log("   Royalty:", (await ratioExNihilo.ROYALTY_BASIS_POINTS()).toString() / 100, "%");
  console.log("   Entity:", await ratioExNihilo.ENTITY_NAME());
  console.log("   EIN:", await ratioExNihilo.EIN());
  console.log("   Wyoming Filing:", await ratioExNihilo.WYOMING_FILING());
  console.log("   Motto:", await ratioExNihilo.MOTTO());

  // Wait for block confirmations before verification
  console.log("\n⏳ Waiting for block confirmations...");
  await ratioExNihilo.deploymentTransaction().wait(5);

  // Verify on Etherscan/Polygonscan
  if (process.env.ETHERSCAN_API_KEY) {
    console.log("\n🔍 Verifying contract on Etherscan...");
    try {
      await hre.run("verify:verify", {
        address: contractAddress,
        constructorArguments: [ROYALTY_RECEIVER],
      });
      console.log("✅ Contract verified!");
    } catch (error) {
      console.log("⚠️  Verification failed:", error.message);
    }
  }

  console.log("\n🎉 Deployment complete!");
  console.log("\n📝 Next Steps:");
  console.log("1. Save the contract address:", contractAddress);
  console.log("2. Update metadata JSON files with contract address");
  console.log("3. Upload images and metadata to IPFS");
  console.log("4. Run mint.js to mint the Genesis collection");
  console.log("5. List on OpenSea and other marketplaces");
  console.log("\n🔥💜 RATIO EX NIHILO 💜🔥");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
