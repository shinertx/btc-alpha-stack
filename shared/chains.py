import os
import logging
from dataclasses import dataclass
from typing import List

from web3 import Web3

logger = logging.getLogger(__name__)

@dataclass
class ChainConnection:
    """Represents a connection to a specific blockchain."""
    name: str
    web3: Web3


def _connect(name: str, env_var: str) -> ChainConnection:
    """Create and validate a Web3 connection.

    Parameters
    ----------
    name: str
        Human readable name of the chain.
    env_var: str
        Environment variable holding the RPC URL.

    Returns
    -------
    ChainConnection
        The successfully connected chain.

    Raises
    ------
    ValueError
        If the RPC URL environment variable is missing.
    ConnectionError
        If the connection attempt fails.
    """
    url = os.getenv(env_var)
    if not url:
        logger.error("Environment variable %s not set for %s", env_var, name)
        raise ValueError(f"{env_var} is required for {name}")

    logger.info("Connecting to %s via %s", name, url)
    w3 = Web3(Web3.HTTPProvider(url))
    if not w3.isConnected():
        logger.error("Unable to connect to %s using %s", name, url)
        raise ConnectionError(f"Failed to connect to {name}")
    logger.info("Successfully connected to %s", name)
    return ChainConnection(name=name, web3=w3)


def _initialize_connections() -> List[ChainConnection]:
    chain_envs = [
        ("ethereum", "ETH_RPC_URL"),
        ("polygon", "POLYGON_RPC_URL"),
        ("arbitrum", "ARBITRUM_RPC_URL"),
        ("optimism", "OPTIMISM_RPC_URL"),
        ("bsc", "BSC_RPC_URL"),
    ]

    connections: List[ChainConnection] = []
    for name, env in chain_envs:
        connections.append(_connect(name, env))
    return connections


# List of all chain connections available to the application.
ALL_CHAINS: List[ChainConnection] = _initialize_connections()

__all__ = ["ChainConnection", "ALL_CHAINS"]
