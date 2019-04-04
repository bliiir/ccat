# IMPORTS -----------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
import pandas as pd

# Local packages
from ccat.controller.helper import time as t
from ccat.model.database.bucket import Bucket
from ccat.controller.strategy.momentum import Momentum


# TESTS ----------------------------------------------------------------

class Test_strategy_momentum(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Settings
        cls.market_id = 1 # Bitmex
        cls.timeframe_id = 6 # 1d

        cls.count = 500
        cls.time_end = t.now

        cls.reversal_len_ma_top = 40
        cls.reversal_len_ma_bottom = 40
        cls.reversal_prefix = 'reversal'

        cls.extreme_len_ma_top = 40
        cls.extreme_len_ma_bottom = 40
        cls.extreme_prefix = 'extreme'
        cls.extreme_l1 = 1.34
        cls.extreme_l2 = 1.34
        cls.extreme_s1 = 2.5
        cls.extreme_s2 = 1.5

        cls.overtraded_len_rsi = 15
        cls.overtraded_high = 75
        cls.overtraded_low = 31
        cls.overtraded_col = 'price_close'
        cls.overtraded_prefix = 'overtraded'

        # Get a bucket object from Bucket
        cls.bucket = Bucket(
            market_id=cls.market_id,
            timeframe_id=cls.timeframe_id)

        # # Update the bucket table
        # cls.bucket.update(
        #     count = cls.count,
        #     time_end = cls.time_end)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_bucket = cls.bucket.read_all()

        # Instantiate the strategy for the 1d BTCUSD candles on Bitmex
        cls.strategy = Momentum(

            df_bucket = cls.df_bucket,
            reversal_len_ma_top = cls.reversal_len_ma_top,
            reversal_len_ma_bottom = cls.reversal_len_ma_bottom,
            reversal_prefix = cls.reversal_prefix,

            extreme_len_ma_top = cls.extreme_len_ma_top,
            extreme_len_ma_bottom = cls.extreme_len_ma_bottom,
            extreme_prefix = cls.extreme_prefix,
            extreme_l1 = cls.extreme_l1,
            extreme_l2 = cls.extreme_l2,
            extreme_s1 = cls.extreme_s1,
            extreme_s2 = cls.extreme_s2,

            overtraded_len_rsi = cls.overtraded_len_rsi,
            overtraded_high = cls.overtraded_high,
            overtraded_low = cls.overtraded_low,
            overtraded_col = cls.overtraded_col,
            overtraded_prefix = cls.overtraded_prefix)

    # Setup
    def setUp(self):
        pass


    def test_get_all(self):

        df = self.strategy.all()

        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.tail(10)), 10)


    def test_get_signal_only(self):

        signal = self.strategy.signal()

        self.assertIsNotNone(signal)
        self.assertIsInstance(signal, int)
        self.assertIn(signal, [-1, 0, 1])


    def test_get_signals_custom(self):

        cols_in = [
            'id',
            'signal',
            'reversal_signal',
            'extreme_signal',
            'overtraded_signal'
            ]

        rows = 10

        df = self.strategy.signals(cols = cols_in, rows = rows)

        cols_out = df.columns

        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.tail(10)), 10)
        self.assertCountEqual(cols_in, cols_out)


    def test_get_signals_default(self):

        df = self.strategy.signals()

        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.tail(10)), 10)
        self.assertIn(f'{self.extreme_prefix}_signal', df.columns)
        self.assertIn(f'{self.overtraded_prefix}_signal', df.columns)
        self.assertIn(f'{self.reversal_prefix}_signal', df.columns)


    def test_extreme(self):

        df = self.strategy.extreme()

        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.tail(10)), 10)
        self.assertIn(f'{self.extreme_prefix}_long', df.columns)
        self.assertIn(f'{self.extreme_prefix}_short', df.columns)
        self.assertIn(f'{self.extreme_prefix}_signal', df.columns)


    def test_overtraded(self):

        df = self.strategy.overtraded()

        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.tail(10)), 10)
        self.assertIn(f'{self.overtraded_prefix}_long', df.columns)
        self.assertIn(f'{self.overtraded_prefix}_short', df.columns)
        self.assertIn(f'{self.overtraded_prefix}_signal', df.columns)


    def test_reversal(self):

        df = self.strategy.reversal()

        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.tail(10)), 10)
        self.assertIn(f'{self.reversal_prefix}_long', df.columns)
        self.assertIn(f'{self.reversal_prefix}_short', df.columns)
        self.assertIn(f'{self.reversal_prefix}_signal', df.columns)



# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()
