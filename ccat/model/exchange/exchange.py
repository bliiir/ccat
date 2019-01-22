'''
------------------------------------------------------------------------
    EXCHANGE.PY
------------------------------------------------------------------------
Interface layer for the 'exchange' table in the database and exchange
related operations such as fetching data from the reading and writing
data from the exchanges, executing orders, getting balances etc
------------------------------------------------------------------------
'''

'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard library imports
import json
import os

# Third party imports
import pandas as pd
import ccxt

# Local application imports
from ccat.model.database.client import Client

'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Exchange():

    def __init__(self, exchange_id):

        self.id = exchange_id

        sql = f'SELECT * FROM exchange WHERE id = {self.id}'
        df = pd.read_sql(sql=sql, con = Client.get())

        self.name = df.name[0]
        self.api_key = os.environ[df.api_key[0]]
        self.api_secret = os.environ[df.api_secret[0]]

    def client(self):

        try:
            if self.id==3:
                self.client = ccxt.bitmex(
                    {'apiKey': self.api_key,
                    'secret': self.api_secret})

            ##### ADD MORE EXCHANGES HERE #####

            else:
                raise Exception('''\
                    CLIENT ERROR: Exchange not connected yet''')

        except Exception as e:
            print(e)
            raise e

        # Enable rate limiting to ensure we don't get locked out
        self.client.enableRateLimit = True

        return self.client


'''
------------------------------------------------------------------------
    UNITTEST
------------------------------------------------------------------------
'''
# https://docs.python.org/3.7/library/unittest.html#module-unittest

import unittest


class Test_exchange(unittest.TestCase):

    def setUp(self):

        import ccat.model.database.market as market

        self.market_id = 1
        self.market = market.Market(market_id=self.market_id)

        # Get exchange_id from market_id
        self.exchange_id = self.market.get_exchange_id()

        # Create an exchange instance
        self.exchange = Exchange(exchange_id=self.exchange_id)

        # Get an exchange client
        self.exchange_client = self.exchange.client()


    def test_get_exchange(self):
        self.assertIsNotNone(self.exchange)

    def test_get_exchange_client(self):
        self.assertIsNotNone(self.exchange_client)

    def test_get_exchange_client_name(self):
        self.assertEqual(self.exchange.name, 'Bitmex')

    def test_get_exchange_client_url(self):
        self.assertEqual(self.exchange_client.urls['www'], 'https://www.bitmex.com')


    def test_get_candles(self):

        limit = 500

        # Fetch the 1h BTC candles
        candles = self.exchange_client.fetchOHLCV(
            'BTC/USD',
            '1h',
            limit=limit,
            since=self.exchange.client.parse8601 ('2018-11-5T00:00:00Z'))

        df = pd.DataFrame(candles)
        df.columns = ['time_close', 'price_open', 'price_high', 'price_low', 'price_close', 'volume' ]
        print(df.tail(10))

        # Check the df is not empty
        self.assertIsNotNone(df)

        # Check that df is a dataframe
        self.assertIsInstance(df, pd.DataFrame)

        # Check length of dataframe
        self.assertTrue(len(df) == limit)

    def test_create_order(self):
        self.new_order = self.exchange_client.create_order(
            side='sell',
            symbol='BTC/USD',
            type='market',
            amount=1,
            )
        print('New order: ', self.new_order)


'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()


