'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest
import pdb

# Third party packages
import pandas as pd

# Local packages
from ccat import config
from ccat.model.database.bucket import Bucket
from ccat.controller.signal.extreme import Extreme


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Test_controller_signal_extreme_real_data(unittest.TestCase):
    '''Test if the extreme module returns the expexted results
    '''

    @classmethod
    def setUpClass(cls):

        cls.bucket = Bucket(
            market_id = 1,
            timeframe_id = 6)

        # cls.bucket.update()

        cls.df_bucket = cls.bucket.read_all()

        cls.extreme = Extreme(
            df_bucket = cls.df_bucket,
            len_ma_top= 40,
            len_ma_bottom = 40,
            suffix = 'extreme')


    def test_extreme_signal(self):

        signal = self.extreme.signal()
        self.assertIn(signal, [-1, 0, 1])


    def test_extreme_get_custom_rows(self):

        cols = ['id', 'time_close_dt', 'signal_extreme']
        rows = 5

        df = self.extreme.get(
            cols = cols,
            rows = rows)

        self.assertEqual(len(df), rows)
        self.assertCountEqual(df.columns, cols)


    def test_extreme_get_custom_columns(self):

        cols = [
            # 'time_close',
            'time_close_dt',
            # 'abs_top_ema',
            # 'abs_bottom_ema',
            # 'long_extreme',
            # 'short_extreme',
            'signal_extreme'
            ]

        df = self.extreme.get(cols = cols)
        self.assertCountEqual(df.columns, cols)


    def test_extreme_get_default(self):

        cols = [
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
            'abs_total',
            'abs_body',
            'abs_top',
            'abs_bottom',
            'pct_body',
            'pct_top',
            'pct_bottom',
            'abs_top_ema',
            'abs_bottom_ema',
            'long_extreme',
            'short_extreme',
            'signal_extreme']

        df = self.extreme.get()

        self.assertCountEqual(df.columns, cols)
        self.assertEqual(10, len(df.tail(10)))


    def test_extreme_short(self):

        df = self.extreme.short()

        cols = ['id', 'short_extreme']

        self.assertCountEqual(df.columns, cols)
        self.assertEqual(len(df.tail(10)), 10)


    def test_extreme_long(self):

        df = self.extreme.long()

        cols = ['id', 'long_extreme']

        self.assertCountEqual(df.columns, cols)
        self.assertEqual(len(df.tail(10)), 10)


    def test_extreme_instance_attributes(self):
        self.assertEqual(self.extreme.len_ma_top, 40)
        self.assertEqual(self.extreme.len_ma_bottom, 40)
        self.assertEqual(self.extreme.suffix, 'extreme')
        self.assertEqual(len(self.extreme.df_bucket.tail(10)), 10)
        self.assertEqual(len(self.extreme.df_heights.tail(10)), 10)
        self.assertEqual(len(self.extreme.df_ema_top.tail(10)), 10)
        self.assertEqual(len(self.extreme.df_ema_bottom.tail(10)), 10)


    def test_extreme_object_has__methods(self):
        self.assertIn('get', dir(self.extreme))
        self.assertIn('long', dir(self.extreme))
        self.assertIn('short', dir(self.extreme))



'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()