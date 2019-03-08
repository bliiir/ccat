'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest

# Third party packages
import pandas as pd

# Local packages
from ccat.model.database.bucket import Bucket
from ccat.controller.signal.reversal import Reversal


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Test_controller_signal_reversal_real_data(unittest.TestCase):
    '''Test if the overtraded module returns the expexted results by
    exposing it to a known dataset
    '''

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get dataframe with all the market and timeframe data
        cls.df_bucket = cls.b.read_all()

        # Number of candles/buckets to include in the rsi calculation
        len_rsi = 20

        # Get an instance of the Overtraded object
        cls.reversal = Reversal(
            df_bucket = cls.df_bucket,
            len_ma_top = 40,
            len_ma_bottom = 40,
            suffix = 'reversal')


    def test_reversal_get_current_signal(self):
        df = self.reversal.get(cols = ['signal_reversal'], rows = 1)
        signal = df.iat[0,1]
        # print('\nREVERSAL CURRENT SIGNAL', signal)
        self.assertIn(signal, [0, 1, -1])


    def test_reversal_get_custom_columns(self):

        cols = [
            'id',
            'signal_reversal']

        df = self.reversal.get(cols)

        self.assertCountEqual(cols, df.columns)
        self.assertEqual(10, len(df.head(10)))


    def test_reversal_get_default(self):

        cols = [
            'id',
            'abs_top_ema',
            'abs_bottom_ema',
            'crossover',
            'crossunder',
            'cross',
            'long_wix',
            'short_wix',
            'signal_wix']


    def test_reversal_object_has_time_series_data(self):

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
            'time_close_dt']

        self.assertIn('id', self.reversal.df_bucket.columns)
        self.assertCountEqual(cols, self.reversal.df_bucket.columns)
        self.assertEqual(10, len(self.reversal.df_bucket.tail(10)))


    def test_reversal_object_has_vars(self):
        self.assertIn('len_ma_top', vars(self.reversal))
        self.assertIn('len_ma_bottom', vars(self.reversal))


    def test_reversal_object_has_get_method(self):
        self.assertIn('get', dir(self.reversal))



'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()