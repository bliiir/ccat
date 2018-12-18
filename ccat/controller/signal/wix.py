'''
------------------------------------------------------------------------
    WIX.PY
------------------------------------------------------------------------
Signals long (1) or short (-1) or no action (0) based on crossovers of
wick height ema crosses
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
from ccat import bucket
from ccat import height
from ccat import ema
from ccat import sma
from ccat import df_x_df
from ccat import config as cnf


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Wix:
    '''Signals long (1) or short (-1) or no action (0) based on
    crossovers of wick height ema crosses
    '''

    def __init__(
        self,
        df_bucket:pd.DataFrame,
        len_ma_top:int = 40,
        len_ma_bottom:int = 40):

        self.df_bucket = df_bucket
        self.len_ma_top = len_ma_top
        self.len_ma_bottom = len_ma_bottom


    def get(self):
        ''' If the top wick ema crosses over the bottom wick ema, return a
        1 (long), if the top wick crosses under the bottom wick ema, return
        a -1(short), otherwise return a 0 (do nothing)
        '''

        # Get the candle heights
        self.df_heights = height.get(self.df_bucket)
        # print(self.df_heights)

        ## EMA: ema(df_heights)
        self.df_ema_top = ema.get(
            df_in=self.df_heights,
            id='id',
            data=self.df_heights.columns[3],
            n = self.len_ma_top,
            prefix = self.df_heights.columns[3])

        self.df_ema_bottom = ema.get(
            df_in=self.df_heights,
            id='id',
            data=self.df_heights.columns[4],
            n = self.len_ma_bottom,
            prefix = self.df_heights.columns[4])

        self.df_out = df_x_df.get(
            df_in_1 = self.df_ema_top,
            df_in_2 = self.df_ema_bottom,
            col_1 = self.df_ema_top.columns[1],
            col_2 = self.df_ema_bottom.columns[1])


        # Calculate crossover
        self.df_out['long_wix'] = np.where(self.df_out.iloc[ :, 3], 1, 0)
        self.df_out['short_wix'] = np.where(self.df_out.iloc[ :, 4], -1, 0)

        cols = [
            'long_wix',
            'short_wix']

        # Compiled signal
        self.df_out['signal_wix'] = self.df_out[cols].sum(axis=1)

        return self.df_out



'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    # Variables
    market_id = 1
    timeframe_id = 6
    time_end=cnf.now()
    count = 500
    len_ma_top = 10
    len_ma_bottom = 10

    # Read candle data
    b= bucket.Bucket(market_id=market_id, timeframe_id=timeframe_id)
    df_bucket = b.read_until(count = count, time_end = time_end)

    # Create Wix instance
    w = Wix(
        df_bucket = df_bucket,
        len_ma_top = len_ma_top,
        len_ma_bottom = len_ma_bottom)

    print(w.get())
    # w.get()






