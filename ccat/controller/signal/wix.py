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
        market_id=1,
        timeframe_id=6,
        len_ema_top=40,
        len_ema_bottom=40):


        self.market_id = market_id
        self.timeframe_id = timeframe_id
        self.len_ema_top = len_ema_top
        self.len_ema_bottom = len_ema_bottom
        self.bucket = bucket.Bucket(market_id=market_id,timeframe_id=timeframe_id)


    def get(self, time_end = cnf.now()):
        ''' If the top wick ema crosses over the bottom wick ema, return a
        1 (long), if the top wick crosses under the bottom wick ema, return
        a -1(short), otherwise return a 0 (do nothing)
        '''

        self.df_bucket = self.bucket.read_until(count=500, time_end = time_end)
        self.df_heights = height.get(self.df_bucket)

        ## EMA: ema(df_heights)
        self.df_ema_top = ema.get(
            df_in=self.df_heights,
            id='id',
            data=self.df_heights.columns[3],
            n = self.len_ema_top,
            prefix = self.df_heights.columns[3])

        self.df_ema_bottom = ema.get(
            df_in=self.df_heights,
            id='id',
            data=self.df_heights.columns[4],
            n = self.len_ema_bottom,
            prefix = self.df_heights.columns[4])

        self.df_in = df_x_df.get(
            df_in_1 = self.df_ema_top,
            df_in_2 = self.df_ema_bottom,
            col_1 = self.df_ema_top.columns[1],
            col_2 = self.df_ema_bottom.columns[1])

        # Initialize df_out dataframe
        self.df_out = pd.DataFrame()

        # Calculate crossover
        self.df_out['long'] = np.where(self.df_in.iloc[ :, 3], True, False)
        self.df_out['short'] = np.where(self.df_in.iloc[ :, 4], True, False)
        self.df_out['signal'] = np.where(self.df_in.iloc[ :, 3], 1, np.where(self.df_in.iloc[ :, 4], -1, 0))

        return self.df_out


    def signal(self, time_end = cnf.now()):

        # Get the dataframe
        self.get(time_end = cnf.now())

        return self.df_out.iloc[-1]['signal']




'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    # Create Wix instance
    w = Wix(market_id=1, timeframe_id=6, len_ema_top=40, len_ema_bottom=40)

    # Get last signal
    print(w.get(time_end = cnf.now()))
    print(w.signal(time_end = cnf.now()))






