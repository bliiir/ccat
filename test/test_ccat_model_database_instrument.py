# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
pass

# Local packages
from ccat.model.database.instrument import Instrument



# TESTS ----------------------------------------------------------------


class Test_model_database_instrument(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.market_id = 1
        cls.my_instrument = Instrument(market_id=1)

    def test_get(self):
        instrument = self.my_instrument.get()
        self.assertIsNotNone(instrument)
        self.assertIn('asset_base_id', dir(instrument))
        self.assertIn('market_id', dir(instrument))

    def test_is_not_none(self):
        self.assertIsNotNone(self.my_instrument)

    def test_market_symbol_native(self):
        self.assertEqual(
            self.my_instrument.market_symbol_native,
            'XBTUSD')

    def test_market_symbol_ccxt(self):
        self.assertEqual(
            self.my_instrument.market_symbol_ccxt,
            'BTC/USD')

    def test_exchange_id(self):
        self.assertEqual(
            self.my_instrument.exchange_id,
            3)


# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()

