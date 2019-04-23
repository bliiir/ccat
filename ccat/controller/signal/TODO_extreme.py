'''
------------------------------------------------------------------------
    OVERTRADED.PY
------------------------------------------------------------------------
These indicators tells us if an asset is over- or under bought according
to the RSI indicator. There are four signals

low:
RSI value is lower than the oversold line and the previous two
rsi values are lower than the current

high:
RSI value is higher than the overbought line and the two previous RSI
values are higher than the current

up:
RSI value has crossed back over the oversold line

down:
RSI value has crossed back under the overbought line

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
from ccat import config

from ccat.model.database.bucket import Bucket

import ccat.controller.indicator.rsi as rsi



'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''
class Overtraded:
    '''Signals long (1) when price_close rsi crosses over oversold line,
    or short (-1) when price_close rsi crosses under overbought line
    or no action (0) if neither
    '''

    def __init__(
        self,
        df_bucket:pd.DataFrame,
        len_rsi:int,
        overbought:int,
        oversold:int,
        peak:int,
        trough:int,
        col:str ='price_close'
        ):

        # Instance variables
        self.df_bucket = df_bucket
        self.len_rsi = len_rsi
        self.overbought = overbought
        self.oversold = oversold
        self.peak = peak
        self.trough = trough
        self.col = col

        # print('overbought: ', self.overbought)
        # print('oversold: ', self.oversold)
        # print('peak: ', self.peak)
        # print('trough: ', self.trough)


    def get(self):
        '''Read candle data into a dataframe, calculate RSI values and
        return a pandas dataframe with columns;
            id, rsi, high, low, up, down
        '''

        # Calculate rsi(price_close)
        self.df_out = rsi.get(
            df_in = self.df_bucket,
            id = 'id',
            data = self.col,
            n = self.len_rsi,
            prefix = self.col)

        # print('len_rsi:', self.len_rsi)

        # Get the name of the column with the RSI values
        n = self.df_out.columns[1]



        # Long if rsi is below the oversold line and increasing
        # self.df_out['long_oversold'] = np.where(
        #     (self.df_out[n] < self.oversold) &
        #     (self.df_out[n] > self.df_out[n].shift(1)), 1, 0)

        # # Long if rsi is below the trough line and increasing
        # self.df_out['long_trough'] = np.where(
        #     (self.df_out[n] < self.trough) &
        #     (self.df_out[n] > self.df_out[n].shift(1)), 1, 0)

        ### SHORT ###
        # Short if rsi is above the overbought line, and is decreasing
        self.df_out['short_overbought'] = np.where(
            (self.df_out[n] > self.overbought) &
            (self.df_out[n] < self.df_out[n].shift(1)),
            -1, 0)

        # Eliminate all but the first signal
        self.df_out['short_overbought'] = np.where(
            (self.df_out['short_overbought'] == -1) &
            (self.df_out['short_overbought'].shift(1) != -1),
            -1, 0)


        # # Short if rsi is above the peak line and decreasing
        # self.df_out['short_peak'] = np.where(
        #     (self.df_out[n] > self.peak), -1, 0)





        # # Short if rsi is above the peak line and decreasing
        # self.df_out['short_peak'] = np.where(
        #     (self.df_out[n] > self.peak) &
        #     (self.df_out[n] < self.df_out[n].shift(1)),
        #     -1, 0)

        #  # Long if rsi is below the oversold line and increasing
        # self.df_out['long_oversold'] = np.where(
        #     (self.df_out[n] < self.oversold) &
        #     (self.df_out[n] > self.df_out[n].shift(1)),
        #     1, 0)

        # # Short if rsi is above the overbought line, and is decreasing
        # self.df_out['short_overbought'] = np.where(
        #     (self.df_out[n] > self.overbought) &
        #     (self.df_out[n] < self.df_out[n].shift(1)),
        #     -1, 0)


        # Compile signal
        cols = ['short_overbought']

        # # Compile signal
        # cols = [
        #     'long_trough',
        #     'long_oversold',
        #     'short_peak',
        #     'short_overbought']

        # self.df_out['signal_overtraded'] = self.df_out[cols].sum(axis=1)

        return self.df_out