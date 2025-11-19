/**
 * Deployment script for Weaponized Legacy Smart Contracts
 * Deploy CryptographicTrust, CoreProtocolAuthority, and ChaosToken
 */

const hre = require("hardhat");

async function main() {
  console.log("🔥 Deploying Weaponized Legacy Contracts...\n");
  
  // Get deployer account
  const [deployer] = await hre.ethers.getSigners();
  const balance = await hre.ethers.provider.getBalance(deployer.address);
  
  console.log("Deploying contracts with account:", deployer.address);
  console.log("Account balance:", hre.ethers.formatEther(balance), "ETH\n");
  
  // Deploy CryptographicTrust
  console.log("1. Deploying CryptographicTrust...");
  const CryptoTrust = await hre.ethers.getContractFactory("CryptographicTrust");
  const cryptoTrust = await CryptoTrust.deploy(
    deployer.address, // treasury address
    deployer.address  // founder address
  );
  await cryptoTrust.waitForDeployment();
  const cryptoTrustAddress = await cryptoTrust.getAddress();
  console.log("   ✓ CryptographicTrust deployed to:", cryptoTrustAddress);
  
  // Deploy CoreProtocolAuthority
  console.log("\n2. Deploying CoreProtocolAuthority...");
  const CoreAuth = await hre.ethers.getContractFactory("CoreProtocolAuthority");
  const coreAuth = await CoreAuth.deploy();
  await coreAuth.waitForDeployment();
  const coreAuthAddress = await coreAuth.getAddress();
  console.log("   ✓ CoreProtocolAuthority deployed to:", coreAuthAddress);
  
  // Deploy ChaosToken
  console.log("\n3. Deploying ChaosToken...");
  const ChaosToken = await hre.ethers.getContractFactory("ChaosToken");
  const chaosToken = await ChaosToken.deploy(deployer.address);
  await chaosToken.waitForDeployment();
  const chaosTokenAddress = await chaosToken.getAddress();
  console.log("   ✓ ChaosToken deployed to:", chaosTokenAddress);
  
  // Display summary
  console.log("\n" + "=".repeat(60));
  console.log("✓ All contracts deployed successfully!");
  console.log("=".repeat(60));
  console.log("\nContract Addresses:");
  console.log("-------------------");
  console.log("CryptographicTrust:     ", cryptoTrustAddress);
  console.log("CoreProtocolAuthority:  ", coreAuthAddress);
  console.log("ChaosToken:             ", chaosTokenAddress);
  console.log("\nFounder Address:        ", deployer.address);
  console.log("\nNetwork:                ", hre.network.name);
  
  // Save deployment info
  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      CryptographicTrust: cryptoTrustAddress,
      CoreProtocolAuthority: coreAuthAddress,
      ChaosToken: chaosTokenAddress
    }
  };
  
  const fs = require('fs');
  const deploymentPath = `deployments/${hre.network.name}.json`;
  fs.mkdirSync('deployments', { recursive: true });
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));
  console.log("\n✓ Deployment info saved to:", deploymentPath);
  
  // Verification instructions
  if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
    console.log("\n" + "=".repeat(60));
    console.log("Contract Verification");
    console.log("=".repeat(60));
    console.log("\nTo verify contracts on Etherscan, run:");
    console.log("\nnpx hardhat verify --network", hre.network.name, cryptoTrustAddress, deployer.address, deployer.address);
    console.log("npx hardhat verify --network", hre.network.name, coreAuthAddress);
    console.log("npx hardhat verify --network", hre.network.name, chaosTokenAddress, deployer.address);
  }
  
  console.log("\n🎉 Deployment complete!\n");
}

// Error handling
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error("\n❌ Deployment failed:");
    console.error(error);
    process.exit(1);
  });
