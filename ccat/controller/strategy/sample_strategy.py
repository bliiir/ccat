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
pass

# Third party imports
import pandas as pd
import numpy as np


# Local application imports
from ccat import wix
from ccat import overtraded
from ccat import extreme
# from ccat import height
# from ccat import ema
# from ccat import df_x_df



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

        return self.df_out

'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    from ccat import config as cnf
    from ccat import bucket

    # Create a momentum strategy for the 1d BTCUSD candles on Bitmex

    # Settings
    market_id = 1 # Bitmex
    timeframe_id = 6 # 1d

    time_end = cnf.now()
    count = 500

    len_ma_top_wix = 40
    len_ma_bottom_wix = 40

    len_ma_top_Extreme = 40
    len_ma_bottom_Extreme = 40

    len_rsi = 40

    overbought = 60
    oversold = 40
    peak = 92
    trough = 32

    col = 'price_close'

    # Get a bucket object from Bucket
    b = bucket.Bucket(market_id=market_id, timeframe_id=timeframe_id)

    # Update the table
    b.update()

    # Get a dataframe with all the data for the market and timeframe
    df_bucket = b.read_until(count = count, time_end = time_end)

    m = Momentum(
        df_bucket = df_bucket,
        len_ma_top_wix=len_ma_top_wix,
        len_ma_bottom_wix=len_ma_bottom_wix,
        len_ma_top_Extreme=len_ma_top_Extreme,
        len_ma_bottom_Extreme=len_ma_bottom_Extreme,
        len_rsi=len_rsi,
        overbought=overbought,
        oversold=oversold,
        peak=peak,
        trough=trough,
        col=col)

    df_signal = m.signals()
    df_s = df_signal[['id', 'signal']]
    df_b = df_bucket[['id', 'time_close', 'price_close']]
    # print(df_s)

    df_out = pd.merge(df_b, df_s, on='id')

    print(df_out)






