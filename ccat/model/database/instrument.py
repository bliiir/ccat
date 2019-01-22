'''
------------------------------------------------------------------------
    INSTRUMENT.PY
------------------------------------------------------------------------
I/O interface layer for the 'instrument' table in the database.
'''


'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard library imports
pass

# Third party imports
import pandas as pd

# Local application imports
from ccat.model.database.client import Client


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Instrument():

    def __init__(self, market_id=1):

        self.market_id = market_id

        # Create first bit of the sql string
        sql=f'SELECT * FROM instrument WHERE market_id={self.market_id}'

        instrument = pd.read_sql(sql=sql, con=Client.get())

        # Set attributes of the order object from the instrument data

        self.market_symbol_native = instrument.market_symbol_native[0]
        self.market_symbol_ccxt = instrument.market_symbol_ccxt[0]
        self.market_description = instrument.market_description[0]

        self.pair_id = instrument.pair_id[0]

        self.asset_base_id = instrument.asset_base_id[0]
        self.asset_base_ticker = instrument.asset_base_ticker[0]
        self.asset_base_name = instrument.asset_base_name[0]
        self.asset_quote_id = instrument.asset_quote_id[0]
        self.asset_quote_ticker = instrument.asset_quote_ticker[0]
        self.asset_quote_name = instrument.asset_quote_name[0]

        self.exchange_id = instrument.exchange_id[0]
        self.exchange_name = instrument.exchange_name[0]
        self.exchange_api_key = instrument.exchange_api_key [0]
        self.exchange_api_secret = instrument.exchange_api_secret[0]

    def get(self):
        return self

'''
------------------------------------------------------------------------
    UNITTEST
------------------------------------------------------------------------
'''

import unittest

class Test_instrument(unittest.TestCase):

    def setUp(self):
        self.my_instrument = Instrument(market_id=1)

    def test_is_not_none(self):
        self.assertIsNotNone(self.my_instrument)

    def test_market_symbol_native(self):
        self.assertEqual(self.my_instrument.market_symbol_native, 'XBTUSD')

    def test_market_symbol_ccxt(self):
        self.assertEqual(self.my_instrument.market_symbol_ccxt, 'BTC/USD')

    def test_exchange_id(self):
        self.assertEqual(self.my_instrument.exchange_id, 3)

'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()
