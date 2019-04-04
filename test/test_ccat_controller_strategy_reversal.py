# IMPORTS -----------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
import pandas as pd

# Local packages
from ccat.controller.helper import time as t
from ccat.model.database.bucket import Bucket
from ccat.controller.strategy.reversal import Strategy


# TESTS ----------------------------------------------------------------

class Test_strategy_reversal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Settings
        cls.market_id = 1 # Bitmex
        cls.timeframe_id = 6 # 1d

        cls.count = 500
        cls.time_end = t.now

        cls.len_ma_top = 40
        cls.len_ma_bottom = 40
        cls.prefix = 'reversal'

        # Get a bucket object from Bucket
        cls.bucket = Bucket(
            market_id=cls.market_id,
            timeframe_id=cls.timeframe_id)

        # # Update the bucket table
        # cls.bucket.update(count = cls.count, time_end = cls.time_end)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_bucket = cls.bucket.read_all()

        kwargs = {
            'len_ma_top': cls.len_ma_top,
            'len_ma_bottom': cls.len_ma_bottom,
            'prefix': cls.prefix}

        # Instantiate the strategy for the 1d BTCUSD candles on Bitmex
        cls.strategy = Strategy(df_bucket = cls.df_bucket, **kwargs)


    # Setup
    def setUp(self):
        pass


    def test_get_signal_only(self):

        signal = self.strategy.signal()

        self.assertIsNotNone(signal)
        self.assertIsInstance(signal, int)
        self.assertIn(signal, [-1, 0, 1])


    def test_get_signals_custom(self):

        cols_in = [
            'id',
            'reversal_signal',
            'time_close_ISO',
            'price_close'
            ]

        rows = 10

        df = self.strategy.signals(
            src = True,
            cols = cols_in,
            rows = rows)

        cols_out = df.columns

        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.tail(10)), 10)
        self.assertCountEqual(cols_in, cols_out)


    def test_signals_with_source(self):
        df = self.strategy.signals(src=True)

        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.tail(10)), 10)
        self.assertIn(f'{self.prefix}_long', df.columns)
        self.assertIn(f'{self.prefix}_short', df.columns)
        self.assertIn(f'{self.prefix}_signal', df.columns)
        self.assertIn('time_close', df.columns)
        self.assertIn('price_close', df.columns)


    def test_signals_default(self):
        df = self.strategy.signals()

        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.tail(10)), 10)
        self.assertIn(f'{self.prefix}_long', df.columns)
        self.assertIn(f'{self.prefix}_short', df.columns)
        self.assertIn(f'{self.prefix}_signal', df.columns)



# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()
