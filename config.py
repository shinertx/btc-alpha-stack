"""Configuration module for btc-alpha-stack.

This module loads environment variables using python-dotenv and exposes
commonly used configuration values for trading and execution modules.
Reasonable defaults are provided for development and testing.
"""

from __future__ import annotations

import os
from dotenv import load_dotenv


# Load environment variables from a .env file if present
load_dotenv()


def _get_env(name: str, default: str | None = None, *, required: bool = False) -> str | None:
    """Return the environment variable ``name``.

    Args:
        name: Name of the variable.
        default: Value returned if the variable is not set.
        required: When ``True`` and the variable is missing, a ``RuntimeError``
            is raised.
    """
    value = os.getenv(name, default)
    if required and value is None:
        raise RuntimeError(f"Environment variable '{name}' is required but not set")
    return value


# ---------------------------------------------------------------------------
# Basic application mode
# ---------------------------------------------------------------------------
# ``MODE`` defines how the application should behave.  ``test`` mode uses
# mock contract addresses and allows missing credentials.
MODE: str = _get_env("MODE", "test").lower()


# ---------------------------------------------------------------------------
# Wallet credentials
# ---------------------------------------------------------------------------
# ``PRIVATE_KEY`` is the account's private key used for signing transactions.
# ``PUBLIC_ADDRESS`` is the corresponding public Ethereum address.
PRIVATE_KEY: str | None = _get_env("PRIVATE_KEY", required=MODE != "test")
PUBLIC_ADDRESS: str | None = _get_env("PUBLIC_ADDRESS", required=MODE != "test")


# ---------------------------------------------------------------------------
# RPC endpoints for supported chains
# ---------------------------------------------------------------------------
ETH_RPC_URL: str = _get_env("ETH_RPC_URL", "https://mainnet.infura.io/v3/YOUR_KEY")
POLYGON_RPC_URL: str = _get_env("POLYGON_RPC_URL", "https://polygon-rpc.com")
ARBITRUM_RPC_URL: str = _get_env("ARBITRUM_RPC_URL", "https://arb1.arbitrum.io/rpc")
OPTIMISM_RPC_URL: str = _get_env("OPTIMISM_RPC_URL", "https://mainnet.optimism.io")
BSC_RPC_URL: str = _get_env("BSC_RPC_URL", "https://bsc-dataseed.binance.org/")


# ---------------------------------------------------------------------------
# Flashbots configuration
# ---------------------------------------------------------------------------
# ``FLASHBOTS_KEY`` is the private key used for Flashbots bundles.
# ``FLASHBOTS_ADDRESS`` is the account address associated with that key.
FLASHBOTS_KEY: str | None = _get_env("FLASHBOTS_KEY", required=MODE != "test")
FLASHBOTS_ADDRESS: str | None = _get_env("FLASHBOTS_ADDRESS", required=MODE != "test")


# ---------------------------------------------------------------------------
# Strategy parameters
# ---------------------------------------------------------------------------
# ``TARGET_PROFIT`` is the profit target per trade expressed as a decimal
# (e.g. ``0.01`` is ``1%``).
TARGET_PROFIT: float = float(_get_env("TARGET_PROFIT", "0.01"))

# ``CAPITAL_START`` defines the starting capital allocated to the strategy.
CAPITAL_START: float = float(_get_env("CAPITAL_START", "10000"))


# ---------------------------------------------------------------------------
# Contract addresses
# ---------------------------------------------------------------------------
# For test mode we use mock addresses.  Production addresses can be overridden
# via environment variables.
if MODE == "test":
    WETH_ADDRESS: str = _get_env("WETH_ADDRESS", "0x000000000000000000000000000000000000dead")
    USDC_ADDRESS: str = _get_env("USDC_ADDRESS", "0x000000000000000000000000000000000000beef")
else:
    WETH_ADDRESS: str = _get_env(
        "WETH_ADDRESS", "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    )
    USDC_ADDRESS: str = _get_env(
        "USDC_ADDRESS", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    )


__all__ = [
    "MODE",
    "PRIVATE_KEY",
    "PUBLIC_ADDRESS",
    "ETH_RPC_URL",
    "POLYGON_RPC_URL",
    "ARBITRUM_RPC_URL",
    "OPTIMISM_RPC_URL",
    "BSC_RPC_URL",
    "FLASHBOTS_KEY",
    "FLASHBOTS_ADDRESS",
    "TARGET_PROFIT",
    "CAPITAL_START",
    "WETH_ADDRESS",
    "USDC_ADDRESS",
]
