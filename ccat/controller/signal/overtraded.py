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
from ccat import bucket
from ccat import rsi
from ccat import config as cnf


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
        market_id = 1,
        timeframe_id = 6,
        len_rsi = 40,
        col = 'price_close',
        overbought = 92,
        oversold = 32,
        ):

        self.market_id = market_id
        self.timeframe_id = timeframe_id
        self.len_rsi = len_rsi
        self.col = col
        self.overbought = overbought
        self.oversold = oversold

        # Create a bucket instance
        self.bucket = bucket.Bucket(
            market_id=market_id,
            timeframe_id=timeframe_id)


    def get(self, time_end: int = cnf.now()):
        '''Read candle data into a dataframe, calculate RSI values and
        return a pandas dataframe with columns;
            id, rsi, high, low, up, down
        '''

        # Get the bucket data
        self.df_bucket = self.bucket.read_until(
            count=self.len_rsi*2,
            time_end=time_end)

        # Calculate rsi(price_close)
        self.df_out = rsi.get(
            df_in = self.df_bucket,
            id = 'id',
            data = self.col,
            n = self.len_rsi,
            prefix = self.col)

        # Get the name of the column with the RSI values
        n = self.df_out.columns[1]

        # High
        self.df_out['high'] = (
            (self.df_out[n]>self.overbought) &
            (self.df_out[n]<self.df_out[n].shift(1)))

        # Low
        self.df_out['low'] = (
            (self.df_out[n]<self.oversold) &
            (self.df_out[n]>self.df_out[n].shift(1)))

        # Up
        self.df_out['up'] = (
            (self.df_out[n]>self.oversold) &
            (self.df_out[n].shift(1)< self.oversold))

        # Down
        self.df_out['down'] = (
            (self.df_out[n] < self.overbought) &
            (self.df_out[n].shift(1) > self.overbought))

        # rowcount 0:len_rsi have values based on insufficient data and
        # are therefore removed
        self.df_out = self.df_out.iloc[self.len_rsi:]

        return self.df_out


    def high(self, time_end=cnf.now()):
        '''Returns a boolean indicating if the rsi has
        topped out
        '''
        self.get(time_end=time_end)
        return self.df_out.iloc[-1]['high']


    def low(self, time_end=cnf.now()):
        '''Returns a boolean indicating if the rsi has bottomed out
        '''
        self.get(time_end=time_end)
        return self.df_out.iloc[-1]['low']


    def up(self, time_end=cnf.now()):
        '''Returns a boolean indicating if the rsi has crossed back
        over the oversold threshold
        '''
        self.get(time_end=time_end)
        return self.df_out.iloc[-1]['up']


    def down(self, time_end=cnf.now()):
        '''Returns a boolean indicating if the rsi has crossed back
        under the overbought threshold
        '''
        self.get(time_end=time_end)
        return self.df_out.iloc[-1]['down']


    def signal(self, time_end=cnf.now()):
        '''Returns just the signal. 1 for long, -1 for short and 0 for
        do nothing
        '''
        self.get(time_end=time_end)

        # High
        if self.df_out.iloc[-1]['high']: signal = -1

        # Down
        elif self.df_out.iloc[-1]['down']: signal = -1

        # Low
        elif self.df_out.iloc[-1]['low']: signal = 1

        # Up
        elif self.df_out.iloc[-1]['up']: signal = 1

        else: signal = 0

        return signal



'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    o = Overtraded(
        market_id = 1,
        timeframe_id = 4,
        len_rsi = 40,
        col = 'price_close',
        overbought = 60,
        oversold = 40)

    # print(o)

    # print(o.signal(time_end=cnf.now()))
    # print(o.get(time_end=cnf.now()))

    print('high: ', o.high())
    # print('low: ', o.low())
    # print('up: ', o.up())
    # print('down: ', o.down())




