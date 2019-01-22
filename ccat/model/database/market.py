'''
------------------------------------------------------------------------
    MARKET.PY
------------------------------------------------------------------------
I/O interface layer for the 'market' table in the database.
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

class Market():

    def __init__(self, market_id=1):

        self.market_id = market_id

        sql = f'SELECT * FROM market WHERE id = {self.market_id}'
        df = pd.read_sql(sql=sql, con=Client.get())

        # Set attributes of the market object from the market table
        self.exchange_id = df.exchange_id[0]
        self.pair_id = df.pair_id[0]
        self.symbol_native = df.symbol_native[0]
        self.symbol_ccxt = df.symbol_ccxt[0]
        self.description = df.description[0]


    def get(self):
        return self

    def get_exchange_id(self):
        return self.exchange_id

'''
------------------------------------------------------------------------
    UNITTEST
------------------------------------------------------------------------
'''

import unittest

class Test_market(unittest.TestCase):

    def setUp(self):
        self.market_id = 1
        self.market = Market(self.market_id)

    def test_market_is_not_none(self):
        self.assertIsNotNone(self.market)

    def test_market_get(self):
        self.assertIsNotNone(self.market.get())

    def test_market_get_exchange_id(self):
        self.assertEqual(self.market.get_exchange_id(), 3)

    def test_market_symbol_native(self):
        self.assertEqual(self.market.symbol_native, 'XBTUSD')

    def test_market_symbol_ccxt(self):
        self.assertEqual(self.market.symbol_ccxt, 'BTC/USD')

'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()
