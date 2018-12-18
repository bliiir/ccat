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
class Extreme:
    '''Signals long (1) when price_close rsi crosses over oversold line,
    or short (-1) when price_close rsi crosses under overbought line
    or no action (0) if neither
    '''

    def __init__(
        self,
        df_bucket:pd.DataFrame,
        len_ma_top:int,
        len_ma_bottom:int):

        # Instance variables
        self.df_bucket = df_bucket
        self.len_ma_top = len_ma_top
        self.len_ma_bottom = len_ma_bottom


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
            data = self.df_heights.columns[3],
            n = self.len_ma_top,
            prefix = self.df_heights.columns[3])

        # ema(wix_bottom)
        self.df_ema_bottom = ema.get(
            df_in = self.df_heights,
            id='id',
            data= self.df_heights.columns[4],
            n = self.len_ma_bottom,
            prefix = self.df_heights.columns[4])


    def merge(self):
        ''' Merges the top and bottom wick ema's into a df_out dataframe
        '''

        # Merge the two ema dataframes
        self.df_out = pd.merge(
            self.df_ema_top,
            self.df_ema_bottom,
            on='id')


    def signals(self):
        '''Determines if we are in a dystopic market
        '''

        # Short names
        tw = self.df_heights.columns[3]  # top wick
        bw = self.df_heights.columns[4]  # bottom wick
        twe = self.df_out.columns[1]  # top wick ema
        bwe = self.df_out.columns[2]  # bottom wick ema

        # Set multipliers
        m1 = 1.2
        m2 = 1.2
        m3 = 2 # 2.5

        m4 = 1.34 # 1.2 1.5
        m5 = 1.34 # 1.2 1.5
        m6 = 2

        # Long

        self.df_out['long_extreme'] = np.where(
            (self.df_out[bwe] > self.df_out[bwe].shift(1) * m1) &
            (self.df_out[bwe] > self.df_out[bwe].shift(2) * m2),
            1, 0)

        # Short
        self.df_out['short_extreme'] = np.where(
            (self.df_out[bwe] > self.df_out[bwe].shift(1) * m4) &
            (self.df_out[bwe] > self.df_out[bwe].shift(2) * m5), -1, 0)

        cols = [
            'long_extreme',
            'short_extreme']

        # Compiled signal
        self.df_out['signal_extreme'] = self.df_out[cols].sum(axis=1)


    def get(self):
        '''Runs all the calculation methods in the class based on the
        specific market, timeframe and end-time
        '''

        # Run the setup
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

    from ccat import bucket

    # Variables
    market_id = 1
    timeframe_id = 6

    count = 500
    time_end = cnf.now()

    len_ma_top = 40
    len_ma_bottom = 40


    b= bucket.Bucket(market_id=market_id, timeframe_id=timeframe_id)
    df_bucket = b.read_until(count = count, time_end = time_end)
    # print(df_bucket)

    e = Extreme(
        df_bucket = df_bucket,
        len_ma_top= len_ma_top,
        len_ma_bottom= len_ma_bottom)

    # print(e.get())
    print(e.get())







