'''
------------------------------------------------------------------------
    MOMENTUM.PY
------------------------------------------------------------------------
If extreme, overtraded or wix issue long, or short signals, trigger the
executor
'''


'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard library imports
from datetime import datetime as dt

# Third party imports
import pandas as pd
import numpy as np


# Local application imports
from ccat import wix
from ccat import overtraded
from ccat import extreme



'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Momentum:

    def __init__(self,
            df_bucket:pd.DataFrame,
            len_ma_top_wix:int,
            len_ma_bottom_wix:int,
            len_ma_top_Extreme:int,
            len_ma_bottom_Extreme:int,
            len_rsi:int,
            overbought:int,
            oversold:int,
            peak:int,
            trough:int,
            col:str = 'price_close'):


        # Shared
        self.df_bucket = df_bucket

        # Wix
        self.len_ma_top_wix = len_ma_top_wix
        self.len_ma_bottom_wix = len_ma_bottom_wix

        # Extreme
        self.len_ma_top_Extreme = len_ma_top_Extreme
        self.len_ma_bottom_Extreme = len_ma_bottom_Extreme

        # Overtraded
        self.len_rsi = len_rsi
        self.overbought = overbought
        self.oversold = oversold
        self.peak = peak
        self.trough = trough
        self.col = col


    def wixes(self):
        '''Get Wix signal'''

        w = wix.Wix(
            df_bucket = self.df_bucket,
            len_ma_top = self.len_ma_top_wix,
            len_ma_bottom = self.len_ma_bottom_wix)

        df_wix = w.get()

        return df_wix


    def extreme(self):
        '''Get Extreme signal
        '''

        e = extreme.Extreme(
            df_bucket = self.df_bucket,
            len_ma_top = self.len_ma_top_Extreme,
            len_ma_bottom = self.len_ma_bottom_Extreme)

        df_extreme = e.get()

        return df_extreme


    def overtraded(self):
        '''Get Overtraded signal
        '''

        o = overtraded.Overtraded(
            df_bucket = self.df_bucket,
            len_rsi = self.len_rsi,
            overbought = self.overbought,
            oversold = self.oversold,
            peak = self.peak,
            trough = self.trough,
            col = self.col)

        df_overtraded = o.get()

        return df_overtraded


    def merge(self):
        ''' Merges the top and bottom wick ema's into a df_out dataframe
        '''

        # Initialize df_out dataframe
        self.df_out = pd.DataFrame()

        # Read the individual signals used in the strategy
        df_w = self.wixes()
        df_o = self.overtraded()
        df_e = self.extreme()

        # Merge the three dataframes
        # self.df_out = pd.merge(df_w, df_o, on='id')

        # Merge the three dataframes
        self.df_out = pd.merge(
            pd.merge(
                df_w,
                df_o,
                on='id'),
                    df_e,on='id')

        cols = [
            'signal_wix',
            'signal_overtraded',
            'signal_extreme']

        # Compiled signal
        self.df_out['signal'] = self.df_out[cols].sum(axis=1)


    def signals(self):
        '''Triggers the chain of methods and returns the df_out
        dataframe
        '''

        self.merge()

        self.df_signals = pd.merge(self.df_bucket, self.df_out, on='id')

        return self.df_signals[[
            'id',
            'time_close',
            'price_close',
            'signal']]


    def signal(self):
        '''Gets the most recent signal'''

        # Trigger the chain
        self.signals()
        self.signal = int(self.df_out.iloc[-1]['signal'])
        # print("inside the signal method: ", self.df_out.iloc[-1])

        return self.signal


'''
------------------------------------------------------------------------
    UNITTEST
------------------------------------------------------------------------
'''

import unittest
from ccat import config
from ccat.model.database.bucket import Bucket

class Test_strategy(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Settings
        cls.market_id = 1 # Bitmex
        cls.timeframe_id = 6 # 1d

        cls.count = 500
        cls.time_end = config.now()

        cls.len_ma_top_wix = 40
        cls.len_ma_bottom_wix = 40

        cls.len_ma_top_Extreme = 40
        cls.len_ma_bottom_Extreme = 40

        cls.len_rsi = 40

        cls.overbought = 60
        cls.oversold = 40
        cls.peak = 92
        cls.trough = 32

        cls.col = 'price_close'

        # Get a bucket object from Bucket
        cls.bucket = Bucket(
            market_id=cls.market_id,
            timeframe_id=cls.timeframe_id)

        # Update the table
        # bucket.update()

        # Get a dataframe with all the data for the market and timeframe
        cls.df_bucket = cls.bucket.read_until(
            count = cls.count,
            time_end = cls.time_end)

        # Instantiate the strategy
        cls.strategy = Momentum(
            df_bucket = cls.df_bucket,
            len_ma_top_wix=cls.len_ma_top_wix,
            len_ma_bottom_wix=cls.len_ma_bottom_wix,
            len_ma_top_Extreme=cls.len_ma_top_Extreme,
            len_ma_bottom_Extreme=cls.len_ma_bottom_Extreme,
            len_rsi=cls.len_rsi,
            overbought=cls.overbought,
            oversold=cls.oversold,
            peak=cls.peak,
            trough=cls.trough,
            col=cls.col)


        # Create a momentum strategy for the 1d BTCUSD candles on Bitmex



    # Setup
    def setUp(self):
        pass


    def test_get_signals(self):

        # Get the signals dataframe
        self.df_signals = self.strategy.signals()

        # Test that it is not empty
        self.assertIsNotNone(self.df_signals)

        # Test that it is a dataframe
        self.assertIsInstance(self.df_signals, pd.DataFrame)

        # Test that it is has the correct length
        self.assertEqual(len(self.df_signals), 500)


    def test_get_signal(self):

        # Get the signal integer
        self.signal = self.strategy.signal()

        # Test that it is not empty
        self.assertIsNotNone(self.signal)

        # Test that it is an integer
        self.assertIsInstance(self.signal, int)

        # Test that it is a valid signal
        self.assertIn(self.signal, [-1, 0, 1])



'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()





