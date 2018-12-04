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
from ccat import bucket
from ccat import height
from ccat import ema
from ccat import config as cnf


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''
class Extreme:
    '''Signals long (1) when price_close rsi crosses over oversold line,
    or short (-1) when price_close rsi crosses under overbought line
    or no action (0) if neither
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

        self.bucket = bucket.Bucket(
            market_id=market_id,
            timeframe_id=timeframe_id)


    def buckets(self, time_end: int = cnf.now()):
        '''Gets OHLCV data'''

        self.df_bucket = self.bucket.read_until(
            count = 500,
            time_end = time_end)

    def features(self):
        '''Fetches the candle part heights
        '''
        self.df_heights = height.get(self.df_bucket)


    def indicators(self):
        '''Calculates the emas for the top and bottom wick heights
        '''

        # ema(wix_top)
        self.df_ema_top = ema.get(
            df_in=self.df_heights,
            id='id',
            data=self.df_heights.columns[3],
            n = self.len_ema_top,
            prefix = self.df_heights.columns[3])

        # ema(wix_bottom)
        self.df_ema_bottom = ema.get(
            df_in=self.df_heights,
            id='id',
            data=self.df_heights.columns[4],
            n = self.len_ema_bottom,
            prefix = self.df_heights.columns[4])


    def merge(self):
        ''' Merges the top and bottom wick ema's into a df_out dataframe
        '''

        # Initialize df_out dataframe
        self.df_out = pd.DataFrame()

        # Merge the two ema dataframes
        self.df_out = pd.merge(
            self.df_ema_top,
            self.df_ema_bottom,
            how='left',
            left_on='id',
            right_on='id',)


    def signals(self):
        '''Determines if we are in a dystopic market
        '''

        # Short names
        c1 = self.df_out.columns[1]  # top wick ema
        c2 = self.df_out.columns[2]  # bottom wick ema

        # Set multipliers
        m1 = 1.1  #1.34
        m2 = 1.1  #1.34
        m3 = 1.1  #1.3
        m4 = 1.1  #1.2

        # Euphoria boolean column
        self.df_out['euphoria'] = (
            (self.df_out[c1] > self.df_out[c1].shift(1) * m1) &
            (self.df_out[c1] > self.df_out[c1].shift(2) * m2) &
            (self.df_out[c1] > self.df_out[c2]))

        # Dystopi boolean column
        self.df_out['dystopia'] = (
            (self.df_out[c2] > self.df_out[c2].shift(1) * m3) &
            (self.df_out[c2] > self.df_out[c2].shift(2) * m4) &
            (self.df_out[c2] > self.df_out[c1]))

        # Add a signal column with -1 for short, 1 for long and 0 for
        # no action
        self.df_out['signal'] = np.where(
            self.df_out['euphoria'], -1,
            np.where(self.df_out['dystopia'], 1, 0))


    def get(self, time_end: int = cnf.now()):
        '''Runs all the calculation methods in the class based on the
        specific market, timeframe and end-time
        '''

        # Run the setup
        self.buckets(time_end=time_end)
        self.features()
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
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    e = Extreme(
        market_id=1,
        timeframe_id=6,
        len_ema_top=40,
        len_ema_bottom=40)

    print(e.get())
    print(e.signal())





