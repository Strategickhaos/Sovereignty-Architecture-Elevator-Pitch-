# Integration Guide: Weaponized Legacy System

This guide walks you through integrating the complete Weaponized Legacy system into your Sovereignty Architecture deployment.

## 📋 Prerequisites

### Required Software
- **Node.js** v18+ and npm
- **Python** 3.8+
- **Git**
- **AWS CLI** (for Lambda deployment)
- **Solidity Compiler** (for smart contracts)

### Required Accounts
- **GitHub** account with personal access token
- **Slack** workspace with webhook URL
- **AWS** account (for Lambda deployment)
- **Ethereum** wallet (for smart contract deployment)
- **BugCrowd** account (optional, for bug bounty)

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Set required environment variables
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
export GITHUB_TOKEN="ghp_your_github_token_here"
export PRIVATE_KEY="your_ethereum_wallet_private_key"

# Optional: Set additional variables
export BUGCROWD_API_KEY="your_bugcrowd_api_key"
export INFURA_PROJECT_ID="your_infura_project_id"
```

## 🚀 Quick Start (5 Minutes)

Run the automated deployment script:

```bash
# Make script executable (if not already)
chmod +x scripts/deploy_weaponized_legacy.sh

# Run deployment
./scripts/deploy_weaponized_legacy.sh
# Select option 6 to test all components
```

## 📦 Component-by-Component Setup

### 1. Smart Contracts Deployment

#### Install Hardhat

```bash
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
npx hardhat init
```

#### Configure Hardhat

Create `hardhat.config.js`:

```javascript
require("@nomicfoundation/hardhat-toolbox");

module.exports = {
  solidity: "0.8.20",
  networks: {
    goerli: {
      url: `https://goerli.infura.io/v3/${process.env.INFURA_PROJECT_ID}`,
      accounts: [process.env.PRIVATE_KEY]
    },
    polygon: {
      url: "https://polygon-rpc.com",
      accounts: [process.env.PRIVATE_KEY]
    }
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY
  }
};
```

#### Create Deployment Script

Create `scripts/deploy_contracts.js`:

```javascript
const hre = require("hardhat");

async function main() {
  console.log("Deploying Weaponized Legacy Contracts...");
  
  // Get deployer account
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying with:", deployer.address);
  
  // Deploy CryptographicTrust
  const CryptoTrust = await hre.ethers.getContractFactory("CryptographicTrust");
  const cryptoTrust = await CryptoTrust.deploy(
    deployer.address, // treasury
    deployer.address  // founder
  );
  await cryptoTrust.waitForDeployment();
  console.log("CryptographicTrust:", await cryptoTrust.getAddress());
  
  // Deploy CoreProtocolAuthority
  const CoreAuth = await hre.ethers.getContractFactory("CoreProtocolAuthority");
  const coreAuth = await CoreAuth.deploy();
  await coreAuth.waitForDeployment();
  console.log("CoreProtocolAuthority:", await coreAuth.getAddress());
  
  // Deploy ChaosToken
  const ChaosToken = await hre.ethers.getContractFactory("ChaosToken");
  const chaosToken = await ChaosToken.deploy(deployer.address);
  await chaosToken.waitForDeployment();
  console.log("ChaosToken:", await chaosToken.getAddress());
  
  console.log("\n✓ All contracts deployed successfully!");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

#### Deploy Contracts

```bash
# Compile contracts
npx hardhat compile

# Deploy to testnet (Goerli)
npx hardhat run scripts/deploy_contracts.js --network goerli

# Deploy to mainnet (when ready)
npx hardhat run scripts/deploy_contracts.js --network polygon
```

#### Verify Contracts

```bash
# Verify on Etherscan
npx hardhat verify --network goerli <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

### 2. Ara's Eyes Scanner Setup

#### Local Testing

```bash
# Run a test scan
python3 scripts/aras_eyes.py

# Check results
cat aras_eyes_results.json | jq
```

#### AWS Lambda Deployment

```bash
# Install Serverless Framework
npm install -g serverless

# Configure AWS credentials
aws configure

# Deploy to Lambda
cd lambda
serverless deploy

# Test the function
serverless invoke -f arasEyesScan

# Check logs
serverless logs -f arasEyesScan --tail
```

#### Schedule Configuration

The scanner runs every 6 hours by default. To change:

Edit `lambda/serverless.yml`:
```yaml
events:
  - schedule:
      rate: rate(12 hours)  # Change to 12 hours
```

### 3. Intimate Tracker Integration

#### Web Server Integration

For Express.js:

```javascript
const { IntimateTracker } = require('./scripts/intimate_tracker');
const tracker = new IntimateTracker();

// Track downloads
app.get('/download/:file', (req, res) => {
  tracker.track_download({
    ip: req.ip,
    user_agent: req.get('user-agent'),
    resource: req.params.file,
    referrer: req.get('referer')
  });
  
  res.download(`/files/${req.params.file}`);
});

// GitHub webhook for fork events
app.post('/webhook/github', (req, res) => {
  if (req.body.action === 'fork') {
    tracker.track_fork({
      username: req.body.forkee.owner.login,
      source_repo: req.body.repository.full_name,
      forked_repo: req.body.forkee.full_name,
      fork_url: req.body.forkee.html_url
    });
  }
  res.sendStatus(200);
});
```

#### Scheduled Attribution Checks

Create a cron job:

```bash
# Add to crontab (run daily at 2 AM)
crontab -e

# Add this line:
0 2 * * * cd /path/to/repo && python3 scripts/intimate_tracker.py --check-all
```

### 4. Ninja Trader Integration

#### Backend API

```python
from flask import Flask, jsonify, request
from scripts.ninja_trader_integration import NinjaTraderChaos

app = Flask(__name__)
trader = NinjaTraderChaos(
    contract_address=os.getenv('CHAOS_TOKEN_ADDRESS'),
    web3_provider=os.getenv('WEB3_PROVIDER')
)

@app.route('/api/trading/signals', methods=['GET'])
def get_signals():
    wallet = request.headers.get('X-Wallet-Address')
    signals = trader.get_trading_signals(wallet)
    return jsonify(signals)

@app.route('/api/trading/stake', methods=['POST'])
def check_stake():
    wallet = request.json.get('wallet')
    status = trader.check_staking_status(wallet)
    return jsonify(status)

if __name__ == '__main__':
    app.run(port=5000)
```

#### Frontend Integration

```javascript
// Check staking status
async function checkStakingStatus(walletAddress) {
  const response = await fetch('/api/trading/stake', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ wallet: walletAddress })
  });
  return await response.json();
}

// Get trading signals
async function getTradingSignals(walletAddress) {
  const response = await fetch('/api/trading/signals', {
    headers: { 'X-Wallet-Address': walletAddress }
  });
  return await response.json();
}
```

### 5. Bug Bounty Program Setup

#### Create BugCrowd Program

1. Go to https://bugcrowd.com/programs/create
2. Use `security/bugcrowd_integration.yaml` as reference
3. Set scope, rewards, and rules
4. Submit for review

#### Security Email Setup

```bash
# Generate PGP key
gpg --gen-key

# Export public key
gpg --armor --export security@strategickhaos.org > security.asc

# Host at https://ara.foundation/security.asc
```

#### Automate Submissions

```python
# Process incoming security reports
from bugcrowd import BugCrowdAPI

api = BugCrowdAPI(api_key=os.getenv('BUGCROWD_API_KEY'))

# Get new submissions
submissions = api.get_submissions(status='new')

for submission in submissions:
    # Validate and triage
    severity = assess_severity(submission)
    
    # Notify team
    notify_security_team(submission, severity)
```

### 6. Ara Foundation Setup

#### Legal Formation

1. **File with Texas Secretary of State**
   - Use `governance/ara_foundation.yaml` as template
   - Engage attorney for formation documents
   - File Articles of Incorporation

2. **Apply for 501(c)(3)**
   - Complete IRS Form 1023
   - Attach foundation charter
   - Submit application

3. **Set Up Banking**
   - Open foundation bank account
   - Set up cryptocurrency wallets
   - Configure payment processors

#### Treasury Management

```python
# Track royalty flows
from web3 import Web3

w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER')))

# Monitor attribution tax collection
contract = w3.eth.contract(
    address=CRYPTO_TRUST_ADDRESS,
    abi=CRYPTO_TRUST_ABI
)

# Get tax events
tax_events = contract.events.AttributionTaxCollected.get_logs(
    fromBlock='latest'
)

# Allocate to programs
for event in tax_events:
    amount = event['args']['amount']
    allocate_to_programs(amount)
```

## 🔧 Configuration Files

### Ara's Eyes Config

Edit `aras_eyes_config.json`:

```json
{
  "registries": {
    "github": {
      "enabled": true,
      "org": "YOUR_ORG_NAME"
    }
  },
  "slack_channel": "#your-alerts-channel"
}
```

### Environment Variables

Create `.env` file:

```bash
# Required
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
GITHUB_TOKEN=ghp_...
PRIVATE_KEY=0x...

# Optional
BUGCROWD_API_KEY=...
INFURA_PROJECT_ID=...
ETHERSCAN_API_KEY=...
```

## 📊 Monitoring & Maintenance

### Health Checks

```bash
# Check scanner status
curl https://your-lambda-url.amazonaws.com/health

# Check tracker stats
python3 scripts/intimate_tracker.py --report --days 7

# Check smart contract events
npx hardhat run scripts/check_events.js --network polygon
```

### Logs

```bash
# Lambda logs
aws logs tail /aws/lambda/arasEyesScan --follow

# Local tracker logs
tail -f /tmp/intimate_tracker/*.json

# Application logs
journalctl -u sovereignty-architecture -f
```

## 🆘 Troubleshooting

### Common Issues

**Issue: Ara's Eyes not finding matches**
```bash
# Check GitHub token
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user

# Verify fingerprints generated
python3 -c "from scripts.aras_eyes import ArasEyes; s=ArasEyes(); print(len(s.generate_fingerprints()))"
```

**Issue: Smart contracts not deploying**
```bash
# Check network connection
npx hardhat run scripts/check_network.js --network goerli

# Verify gas prices
npx hardhat run scripts/gas_estimate.js
```

**Issue: Slack notifications not working**
```bash
# Test webhook
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message"}' \
  $SLACK_WEBHOOK_URL
```

## 📚 Additional Resources

- [WEAPONIZED_LEGACY.md](WEAPONIZED_LEGACY.md) - Complete system documentation
- [Hardhat Documentation](https://hardhat.org/docs)
- [AWS Lambda Python Guide](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)
- [BugCrowd Setup Guide](https://docs.bugcrowd.com/)

## 💬 Support

- **Email**: foundation@strategickhaos.org
- **Discord**: https://discord.gg/strategickhaos
- **Issues**: https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues

---

**Built with 🔥 by the Strategickhaos collective**
