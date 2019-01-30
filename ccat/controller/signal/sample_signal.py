'''
------------------------------------------------------------------------
    EXTREME.PY
------------------------------------------------------------------------
Signals if the market is in an extreme euphoric or dystopic state
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
from ccat import config as cnf
from ccat import height
from ccat import ema



'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''
class Sample_signal:
    '''Signals long (1) when price_close rsi crosses over oversold line,
    or short (-1) when price_close rsi crosses under overbought line
    or no action (0) if neither
    '''

    def __init__(
        self,
        df_bucket:pd.DataFrame,
        len_ema_short:int,
        len_ema_long:int):

        # Instance variables
        self.df_bucket = df_bucket
        self.len_ema_short = len_ema_short
        self.len_ema_long = len_ema_long


    def indicators(self):
        '''Calculates the emas for the top and bottom wick heights
        '''

        # ema(wix_top)
        self.df_ema_short = ema.get(
            df_in=self.df_bucket,
            id='id',
            data = self.df_heights.columns['price_close'], # 
            n = self.len_ema_short,
            prefix = self.df_heights.columns['price_close'])

        # ema(wix_bottom)
        self.df_ema_long = ema.get(
            df_in = self.df_bucket,
            id='id',
            data= self.df_heights.columns['price_close'],
            n = self.len_ema_long,
            prefix = self.df_heights.columns['price_close'])


    def merge(self):
        ''' Merges the top and bottom wick ema's into a df_out dataframe
        '''

        # Merge the two ema dataframes
        self.df_out = pd.merge(
            self.df_ema_short,
            self.df_ema_long,
            on='id')


    def signals(self):

        # Short names


        # Long

        self.df_out['long'] = np.where(
            (self.df_out[bwe] > self.df_out[bwe].shift(1) * m1) &
            (self.df_out[bwe] > self.df_out[bwe].shift(2) * m2),
            1, 0)

        # Short
        self.df_out['short'] = np.where(
            (self.df_out[bwe] > self.df_out[bwe].shift(1) * m4) &
            (self.df_out[bwe] > self.df_out[bwe].shift(2) * m5), -1, 0)

        cols = [
            'long',
            'short']

        # Compiled signal
        self.df_out['signal'] = self.df_out[cols].sum(axis=1)


    def get(self):
        '''Runs all the calculation methods in the class based on the
        specific market, timeframe and end-time
        '''

        # Run the setup
        self.indicators()
        self.merge()
        self.signals()

        return self.df_out


    def signal(self, time_end=cnf.now()):
        '''Runs get() and then extracts the signal cell from the last
        row of the dataframe
        '''
        self.get(time_end=time_end)

        # return signal
        return self.df_out.iloc[-1]['signal']


'''
------------------------------------------------------------------------
    UNITTEST
------------------------------------------------------------------------
'''

import unittest

class Test_order(unittest.TestCase):

    from ccat import bucket

    # Setup
    def setUp(self):

        # Variables
        self.market_id = 1
        self.timeframe_id = 6

        self.count = 500
        self.time_end = cnf.now()



'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()



    # b= bucket.Bucket(market_id=market_id, timeframe_id=timeframe_id)
    # df_bucket = b.read_until(count = count, time_end = time_end)
    # # print(df_bucket)

    # e = Extreme(
    #     df_bucket = df_bucket,
    #     len_ma_top= len_ma_top,
    #     len_ma_bottom= len_ma_bottom)

    # # print(e.get())
    # print(e.get())







