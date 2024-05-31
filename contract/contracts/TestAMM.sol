// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TestAMM is ERC20, ReentrancyGuard, Ownable {
    IERC20 public token1;
    IERC20 public token2;

    uint public reserve1;
    uint public reserve2;

    // Governance token distributed to liquidity providers
    IERC20 public governanceToken;
    address public _governanceToken = 0xBafBe8Dc6b88868A7b58F6E5df89c3054dec93bB;
    address public governanceOwner = 0x64a86158D40A628d626e6F6D4e707667048853eb;

    constructor(address _token1, address _token2)
        ERC20("LiquidityProviderToken", "LPT")  Ownable(msg.sender)
    {
        token1 = IERC20(_token1);
        token2 = IERC20(_token2);
        governanceToken = IERC20(_governanceToken);
    }

    // Gas optimization: External functions for external calls
    function addLiquidity(uint _amount1, uint _amount2) external nonReentrant {
        uint balanceToken1 = token1.balanceOf(address(this));
        uint balanceToken2 = token2.balanceOf(address(this));
        uint suppliedToken1 = _amount1;
        uint suppliedToken2 = _amount2;

        require(suppliedToken1 * balanceToken2 == suppliedToken2 * balanceToken1, "Invalid ratio");
        
        token1.transferFrom(msg.sender, address(this), _amount1);
        token2.transferFrom(msg.sender, address(this), _amount2);

        // Mint LP tokens based on the amount of liquidity provided
        uint liquidity = calculateLiquidityAmount(_amount1, _amount2);
        _mint(msg.sender, liquidity);

        // Reward the liquidity provider with governance tokens
        governanceToken.transferFrom(governanceOwner, address(this), liquidity);

        reserve1 += _amount1;
        reserve2 += _amount2;
    }

    function removeLiquidity(uint _amount) external nonReentrant returns (uint, uint) {
        uint totalLiquidity = totalSupply();
        require(_amount <= totalLiquidity, "Invalid amount");

        uint amountToken1 = _amount * reserve1 / totalLiquidity;
        uint amountToken2 = _amount * reserve2 / totalLiquidity;

        _burn(msg.sender, _amount);

        token1.transfer(msg.sender, amountToken1);
        token2.transfer(msg.sender, amountToken2);

        reserve1 -= amountToken1;
        reserve2 -= amountToken2;

        return (amountToken1, amountToken2);
    }

    
    // Utility functions
    function calculateLiquidityAmount(uint _amount1, uint _amount2) private view returns (uint) {
        // Implementation based on the pool's current state and the amounts provided
        // This is a simplified version; in reality, you'd include calculations based on total supply, reserves, etc.
        return _amount1 + _amount2; // Simplified calculation for example purposes
    }
}