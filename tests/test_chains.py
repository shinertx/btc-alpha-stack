import importlib
import sys
from types import SimpleNamespace
from unittest import TestCase
from unittest.mock import patch


class ChainsModuleTest(TestCase):
    def test_connections_created(self):
        class DummyWeb3:
            def __init__(self, provider):
                self.provider = provider
            @staticmethod
            def HTTPProvider(url):
                return url
            def isConnected(self):
                return True

        dummy_module = SimpleNamespace(Web3=DummyWeb3)

        env = {
            'ETH_RPC_URL': 'https://eth',
            'POLYGON_RPC_URL': 'https://polygon',
            'ARBITRUM_RPC_URL': 'https://arbitrum',
            'OPTIMISM_RPC_URL': 'https://optimism',
            'BSC_RPC_URL': 'https://bsc',
        }

        if 'shared.chains' in sys.modules:
            del sys.modules['shared.chains']

        with patch.dict(sys.modules, {'web3': dummy_module}):
            with patch.dict('os.environ', env, clear=True):
                chains = importlib.import_module('shared.chains')
                self.assertEqual(len(chains.ALL_CHAINS), 5)
                names = {c.name for c in chains.ALL_CHAINS}
                self.assertEqual(names, {'ethereum', 'polygon', 'arbitrum', 'optimism', 'bsc'})
