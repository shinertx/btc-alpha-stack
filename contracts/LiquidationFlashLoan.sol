// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

import {IFlashLoanSimpleReceiver} from "@aave/core-v3/contracts/flashloan/interfaces/IFlashLoanSimpleReceiver.sol";
import {IPoolAddressesProvider} from "@aave/core-v3/contracts/interfaces/IPoolAddressesProvider.sol";
import {IPool} from "@aave/core-v3/contracts/interfaces/IPool.sol";

interface ISwapRouter {
    function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external returns (uint[] memory amounts);
}

/**
 * @title LiquidationFlashLoan
 * @notice Executes atomic liquidation using Aave V3 flash loans and swaps collateral for repayment.
 */
contract LiquidationFlashLoan is IFlashLoanSimpleReceiver, ReentrancyGuard, Ownable {
    IPoolAddressesProvider public immutable ADDRESSES_PROVIDER;
    ISwapRouter public swapRouter;
    uint256 public minProfit;

    event MinProfitUpdated(uint256 newMinProfit);

    constructor(IPoolAddressesProvider provider, ISwapRouter router, uint256 _minProfit) {
        ADDRESSES_PROVIDER = provider;
        swapRouter = router;
        minProfit = _minProfit;
    }

    /**
     * @notice Updates the minimum profit requirement.
     * @param _minProfit New profit threshold in asset units.
     */
    function setMinProfit(uint256 _minProfit) external onlyOwner {
        minProfit = _minProfit;
        emit MinProfitUpdated(_minProfit);
    }

    /**
     * @notice Initiates a flash loan.
     * @param asset Address of the asset to borrow.
     * @param amount Amount to borrow.
     * @param params Encoded parameters for liquidation.
     */
    function executeFlashLoan(address asset, uint256 amount, bytes calldata params) external onlyOwner {
        IPool pool = IPool(ADDRESSES_PROVIDER.getPool());
        pool.flashLoanSimple(address(this), asset, amount, params, 0);
    }

    /**
     * @notice Aave callback where the liquidation and swap happen.
     * @param asset Borrowed asset address.
     * @param amount Borrowed amount.
     * @param premium Flash loan fee.
     * @param initiator Initiator of the flash loan.
     * @param params Encoded parameters containing liquidation data.
     * @return True if operation succeeds.
     */
    function executeOperation(
        address asset,
        uint256 amount,
        uint256 premium,
        address initiator,
        bytes calldata params
    ) external override nonReentrant returns (bool) {
        require(msg.sender == address(IPool(ADDRESSES_PROVIDER.getPool())), "caller not pool");
        require(initiator == address(this), "invalid initiator");

        (
            address collateralAsset,
            address debtAsset,
            address user,
            uint256 debtToCover,
            address[] memory swapPath
        ) = abi.decode(params, (address, address, address, uint256, address[]));

        IPool pool = IPool(ADDRESSES_PROVIDER.getPool());

        // Approve debt asset to the pool for liquidation
        IERC20(debtAsset).approve(address(pool), debtToCover);
        pool.liquidationCall(collateralAsset, debtAsset, user, debtToCover, false);

        // Swap seized collateral to the borrowed asset for repayment
        uint collateralBalance = IERC20(collateralAsset).balanceOf(address(this));
        IERC20(collateralAsset).approve(address(swapRouter), collateralBalance);
        swapRouter.swapExactTokensForTokens(collateralBalance, 0, swapPath, address(this), block.timestamp);

        uint amountOwing = amount + premium;
        uint balance = IERC20(asset).balanceOf(address(this));
        require(balance >= amountOwing + minProfit, "insufficient profit");

        IERC20(asset).approve(address(pool), amountOwing);
        return true;
    }

    /**
     * @notice Returns the pool address from the provider.
     */
    function POOL() public view returns (IPool) {
        return IPool(ADDRESSES_PROVIDER.getPool());
    }
}

