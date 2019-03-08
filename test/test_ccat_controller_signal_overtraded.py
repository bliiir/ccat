'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest

# Third party packages
import pandas as pd
import numpy as np

# Local packages
from ccat import config
from ccat.controller.helper import time as t

from ccat.model.database.bucket import Bucket
from ccat.controller.signal.overtraded import Overtraded

'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Test_controller_signal_overtraded_real_data(unittest.TestCase):
    '''Test if the overtraded module returns the expexted results by
    exposing it to a known dataset
    '''

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_bucket = cls.b.read_all()

        # Number of candles/buckets to include in the rsi calculation
        len_rsi = 20

        # Get an instance of the Overtraded object
        cls.overtraded = Overtraded(
            df_bucket = cls.df_bucket,
            len_rsi = len_rsi,
            high = 60,
            low = 40,
            col = 'price_close',
            suffix = 'rsi')

    def test_overtraded_get_current_signals(self):
        df = self.overtraded.get(cols = ['signal_rsi'], rows = 1)
        signal = df.iat[0,1]
        self.assertIn(signal, [0, 1, -1])


    def test_overtraded_get_custom_rows(self):
        df = self.overtraded.get(rows = 1)
        self.assertEqual(len(df), 1)


    def test_overtraded_get_custom_columns(self):

        cols = [
            'id',
            # 'market_id',
            # 'timeframe_id',
            # 'time_open',
            'time_close',
            # 'time_updated',
            # 'price_open',
            # 'price_high',
            'price_close',
            # 'price_low',
            'volume',
            'time_close_dt',
            # 'price_close_rsi_x',
            # 'price_close_rsi_y',
            # 'long_rsi',
            'price_close_rsi',
            # 'short_rsi',
            'signal_rsi']

        df = self.overtraded.get(cols = cols)
        self.assertEqual(len(df.columns), len(cols))
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_get_default(self):
        df = self.overtraded.get()
        self.assertGreater(len(df.columns), 2)
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_short(self):
        df = self.overtraded.short()
        self.assertEqual(len(df.columns), 3)
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_long(self):
        df = self.overtraded.long()
        self.assertEqual(len(df.columns), 3)
        self.assertEqual(len(df.head(10)), 10)


class Test_controller_signal_overtraded_fake_data(unittest.TestCase):
    '''Test if the overtraded module returns the expexted results by
    exposing it to a known dataset
    '''

    @classmethod
    def setUpClass(cls):

        # Number of candles/buckets to include in the rsi calculation
        len_rsi = 20

        # Generate fake data
        x = np.arange(0, 10, 0.1)
        y = (np.sin(x) + 1)/2 *1000

        # Create a dataframe with the fake data
        df = pd.DataFrame({'price_close':y})

        # Set id column = index and then as the id column for merging
        df['id'] = df.index
        df = df[['id', 'price_close']]

        # Get an instance of the Overtraded object
        cls.overtraded = Overtraded(
            df_bucket = df,
            len_rsi = len_rsi,
            high = 60,
            low = 40,
            col = 'price_close',
            suffix = 'rsi')

    def test_overtraded_get(self):

        cols = [
            'id',
            'price_close',
            'price_close_rsi',
            'long_rsi',
            'short_rsi',
            'signal_rsi'
            ]

        df = self.overtraded.get([cols[1], cols[2], cols[5]])
        self.assertEqual(len(df.columns), 4)
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_get_default(self):
        df = self.overtraded.get()
        self.assertGreater(len(df.columns), 2)
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_overbought(self):
        df = self.overtraded.short()
        self.assertEqual(len(df.columns), 3)
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_oversold(self):
        df = self.overtraded.long()
        self.assertEqual(len(df.columns), 3)
        self.assertEqual(len(df.head(10)), 10)


class Test_controller_signal_overtraded_basics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Variables
        market_id = 1
        timeframe_id = 6
        time_end=t.now
        count = 500
        len_rsi = 40
        col = 'price_close'
        high = 60
        low = 40

        # Read candle data
        bucket = Bucket(
            market_id=market_id,
            timeframe_id=timeframe_id)

        cls.df_bucket = bucket.read_until(
            count = count,
            time_end = time_end)

        cls.overtraded = Overtraded(
            df_bucket = cls.df_bucket,
            len_rsi = len_rsi,
            high = high,
            low = low,
            col = col)

        cls.signal = cls.overtraded.get()


    def test_overtraded_signal(self):

        self.df_bucket = pd.DataFrame(
            [
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),

            ],
            columns = ['id', 'price_close'] )


    def test_overtraded_col_names(self):

        col_names = [
            'id',
            'market_id',
            'timeframe_id',
            'time_open',
            'time_close',
            'time_updated',
            'price_open',
            'price_high',
            'price_close',
            'price_low',
            'volume',
            'time_close_dt',
            'price_close_rsi_x',
            'price_close_rsi_y',
            'long_overtraded',
            'price_close_rsi',
            'short_overtraded',
            'signal_overtraded']

        self.assertCountEqual(
            list(self.signal.columns.values),
            col_names)


    def test_overtraded_has_content(self):
        self.assertEqual(len(self.signal.tail(10)), 10)


    def test_overtraded_pandas_dataframe(self):
        self.assertIsInstance(self.signal, pd.DataFrame)


    def test_overtraded_not_none(self):
        self.assertIsNotNone(self.signal)




'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()