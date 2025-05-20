# Utility module for common project tasks

from time import sleep
from typing import Callable, TypeVar, Any

from loguru import logger
from web3 import Web3


T = TypeVar("T")


def setup_logging(level: str = "INFO") -> None:
    """Configure loguru logging for the project."""
    logger.remove()
    logger.add(lambda msg: print(msg, end=""), level=level)


def wei_to_ether(value: int) -> float:
    """Convert Wei to Ether using Web3 utilities.

    Args:
        value: Integer amount in Wei.

    Returns:
        Equivalent amount in Ether as a float.
    """
    try:
        return Web3.fromWei(value, "ether")
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Failed to convert Wei to Ether: {exc}")
        raise


def ether_to_wei(value: float) -> int:
    """Convert Ether to Wei using Web3 utilities.

    Args:
        value: Ether amount as a float.

    Returns:
        Equivalent amount in Wei as an integer.
    """
    try:
        return Web3.toWei(value, "ether")
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Failed to convert Ether to Wei: {exc}")
        raise


def retry_with_backoff(func: Callable[[], T], retries: int = 3, delay: float = 1.0) -> T:
    """Retry a function with exponential backoff.

    Args:
        func: Callable with no arguments that returns a value.
        retries: Maximum number of retries.
        delay: Initial delay in seconds.

    Returns:
        Result of the callable ``func``.

    Raises:
        Exception: Re-raises the last exception if all retries fail.
    """
    current_delay = delay
    for attempt in range(retries):
        try:
            return func()
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"Attempt {attempt + 1} failed with error: {exc}. Retrying in {current_delay} seconds...")
            sleep(current_delay)
            current_delay *= 2
    # final attempt
    return func()


__all__ = [
    "setup_logging",
    "wei_to_ether",
    "ether_to_wei",
    "retry_with_backoff",
]
