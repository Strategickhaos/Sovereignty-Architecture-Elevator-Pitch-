// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title Chaos Token
 * @dev Zero value, zero hype, but tied to Strategickhaos DAOLLC
 * @notice Staking required for trading bot access - pay in love or get static
 */
contract ChaosToken {
    
    string public constant name = "Chaos Token";
    string public constant symbol = "CHAOS";
    uint8 public constant decimals = 18;
    
    uint256 private _totalSupply;
    address public immutable daoAddress;
    
    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowances;
    mapping(address => bool) public isStaked;
    mapping(address => uint256) public stakedAmount;
    mapping(address => uint256) public stakeTimestamp;
    
    // Trading bot access control
    mapping(address => bool) public hasTradingAccess;
    mapping(address => string) public tradingBotEndpoint;
    
    uint256 public constant MINIMUM_STAKE = 1000 * 10**18; // 1000 CHAOS
    uint256 public constant STAKE_DURATION = 30 days;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event TradingAccessGranted(address indexed user);
    event TradingAccessRevoked(address indexed user);
    
    constructor(address _daoAddress) {
        require(_daoAddress != address(0), "Invalid DAO address");
        daoAddress = _daoAddress;
        
        // Initial mint to DAO
        _totalSupply = 1000000 * 10**decimals; // 1 million CHAOS
        _balances[_daoAddress] = _totalSupply;
        
        emit Transfer(address(0), _daoAddress, _totalSupply);
    }
    
    function totalSupply() external view returns (uint256) {
        return _totalSupply;
    }
    
    function balanceOf(address account) external view returns (uint256) {
        return _balances[account];
    }
    
    function transfer(address to, uint256 amount) external returns (bool) {
        _transfer(msg.sender, to, amount);
        return true;
    }
    
    function allowance(address owner, address spender) external view returns (uint256) {
        return _allowances[owner][spender];
    }
    
    function approve(address spender, uint256 amount) external returns (bool) {
        _approve(msg.sender, spender, amount);
        return true;
    }
    
    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        uint256 currentAllowance = _allowances[from][msg.sender];
        require(currentAllowance >= amount, "Transfer amount exceeds allowance");
        
        _transfer(from, to, amount);
        _approve(from, msg.sender, currentAllowance - amount);
        
        return true;
    }
    
    /**
     * @notice Stake CHAOS tokens to gain trading bot access
     * @param amount Amount to stake (must be >= MINIMUM_STAKE)
     */
    function stake(uint256 amount) external {
        require(amount >= MINIMUM_STAKE, "Insufficient stake amount");
        require(_balances[msg.sender] >= amount, "Insufficient balance");
        require(!isStaked[msg.sender], "Already staked");
        
        _balances[msg.sender] -= amount;
        stakedAmount[msg.sender] = amount;
        stakeTimestamp[msg.sender] = block.timestamp;
        isStaked[msg.sender] = true;
        
        // Grant trading access
        hasTradingAccess[msg.sender] = true;
        
        emit Staked(msg.sender, amount);
        emit TradingAccessGranted(msg.sender);
    }
    
    /**
     * @notice Unstake CHAOS tokens after lock period
     */
    function unstake() external {
        require(isStaked[msg.sender], "Not staked");
        require(
            block.timestamp >= stakeTimestamp[msg.sender] + STAKE_DURATION,
            "Stake duration not met"
        );
        
        uint256 amount = stakedAmount[msg.sender];
        
        _balances[msg.sender] += amount;
        stakedAmount[msg.sender] = 0;
        stakeTimestamp[msg.sender] = 0;
        isStaked[msg.sender] = false;
        
        // Revoke trading access
        hasTradingAccess[msg.sender] = false;
        
        emit Unstaked(msg.sender, amount);
        emit TradingAccessRevoked(msg.sender);
    }
    
    /**
     * @notice Register trading bot endpoint
     * @param endpoint API endpoint for trading signals
     */
    function registerTradingBot(string memory endpoint) external {
        require(hasTradingAccess[msg.sender], "No trading access");
        tradingBotEndpoint[msg.sender] = endpoint;
    }
    
    /**
     * @notice Check if address has trading access
     * @param user Address to check
     * @return bool indicating access status
     */
    function checkTradingAccess(address user) external view returns (bool) {
        return hasTradingAccess[user] && isStaked[user];
    }
    
    /**
     * @notice Get trading signals (requires staking)
     * @return string Signal data or "static" if no access
     */
    function getTradingSignals() external view returns (string memory) {
        if (!hasTradingAccess[msg.sender] || !isStaked[msg.sender]) {
            return "STATIC - Stake CHAOS tokens for access";
        }
        
        // In production, this would return actual trading signals
        return "SIGNALS_ACTIVE - Access granted";
    }
    
    // Internal functions
    function _transfer(address from, address to, uint256 amount) internal {
        require(from != address(0), "Transfer from zero address");
        require(to != address(0), "Transfer to zero address");
        require(_balances[from] >= amount, "Insufficient balance");
        
        _balances[from] -= amount;
        _balances[to] += amount;
        
        emit Transfer(from, to, amount);
    }
    
    function _approve(address owner, address spender, uint256 amount) internal {
        require(owner != address(0), "Approve from zero address");
        require(spender != address(0), "Approve to zero address");
        
        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }
}
