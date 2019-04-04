# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
pass

# Local packages
from ccat.model.database.market import Market


# TESTS ----------------------------------------------------------------

class Test_model_database_market(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.market_id = 1
        cls.market = Market(cls.market_id)

    def test_market_is_not_none(self):
        self.assertIsNotNone(self.market)

    def test_market_get(self):
        market = self.market.get()
        self.assertIsNotNone(market)
        self.assertIn('exchange_id', dir(market))

    def test_market_get_exchange_id(self):
        self.assertEqual(self.market.get_exchange_id(), 3)

    def test_market_symbol_native(self):
        self.assertEqual(self.market.symbol_native, 'XBTUSD')

    def test_market_symbol_ccxt(self):
        self.assertEqual(self.market.symbol_ccxt, 'BTC/USD')



# MAIN ----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()