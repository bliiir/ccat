# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
import pandas as pd

# Local packages
from ccat.model.database.market import Market
from ccat.model.exchange.exchange import Exchange


# TESTS --------------------------------------------------------------


class Test_model_exchange_exchange(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.market_id = 1
        cls.market = Market(market_id = cls.market_id)

        # Get exchange_id from market_id
        cls.exchange_id = cls.market.get_exchange_id()

        # Create an exchange instance
        cls.exchange = Exchange(exchange_id = cls.exchange_id)

        # Get an exchange client
        cls.exchange_client = cls.exchange.client()


    def test_get_exchange(self):
        self.assertIsNotNone(self.exchange)

    def test_get_exchange_client(self):
        self.assertIsNotNone(self.exchange_client)

    def test_get_exchange_client_name(self):
        self.assertEqual(self.exchange.name, 'Bitmex')

    def test_get_exchange_client_url(self):
        self.assertEqual(
            self.exchange_client.urls['www'],
            'https://www.bitmex.com')


    def test_get_candles(self):

        limit = 100

        # Fetch the 1h BTC candles
        candles = self.exchange_client.fetchOHLCV(
            'BTC/USD',
            '1h',
            limit=limit,
            since=self.exchange.client.parse8601('2018-11-5T00:00:00Z'))

        df = pd.DataFrame(candles)
        df.columns = [
            'time_close',
            'price_open',
            'price_high',
            'price_low',
            'price_close',
            'volume']

        # Check the df is not empty
        self.assertIsNotNone(df)

        # Check that df is a dataframe
        self.assertIsInstance(df, pd.DataFrame)

        # Check length of dataframe
        self.assertTrue(len(df) == limit)


# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()