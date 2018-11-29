'''
------------------------------------------------------------------------
    STRATEGY.PY
------------------------------------------------------------------------
Feature calculations. Features are datapoints that can be directly
inferred from the raw data
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
from ccat import Bucket
from ccat import feature
from ccat import indicator
from ccat import cross
# from ccat import report


'''
------------------------------------------------------------------------
    SETTINGS
------------------------------------------------------------------------
'''

# Instrument
market_id = 1 # Bitmex BTC/USD
timeframe_id = 6 # minute


# Indicator
len_rsi = 15
len_ema_slow = 32
len_ema_fast = 8
len_ema_rsi_slow = 32
len_ema_rsi_fast = 8
len_ema_top = 40
len_ema_bottom = 40

# Data
col = 'price_close'


bucket = Bucket(market_id=market_id,timeframe_id=timeframe_id)
bucket.update() # Remove this in production ############################

## FEATURES
df_bucket = bucket.read_until(count=500)
df_heights = feature.height(df_bucket)


'''---------------------------------------------------------------------
    INDICATORS
---------------------------------------------------------------------'''

# # RSI: rsi(price_close)
# df_rsi = indicator.rsi(
#     df_in = df_bucket,
#     id='id',
#     data=col,
#     n=len_rsi,
#     prefix = col)


# ## EMA: ema(price_close)
# df_ema_slow = indicator.ema(
#     df_in=df_bucket,
#     id='id', data=col,
#     n = len_ema_slow,
#     prefix = col)

# df_ema_fast = indicator.ema(
#     df_in=df_bucket,
#     id='id',
#     data=col,
#     n = len_ema_fast,
#     prefix = col)


# ## EMA: ema(rsi(price_close))
# df_ema_rsi_slow = indicator.ema(
#     df_in=df_rsi,
#     id='id',
#     data=df_rsi.columns[1],
#     n = len_ema_rsi_slow,
#     prefix = df_rsi.columns[1])

# df_ema_rsi_fast = indicator.ema(
#     df_in=df_rsi,
#     id='id',
#     data=df_rsi.columns[1],
#     n = len_ema_rsi_fast,
#     prefix = df_rsi.columns[1])

## EMA: ema(df_heights)
df_ema_top = indicator.ema(
    df_in=df_heights,
    id='id',
    data=df_heights.columns[3],
    n = len_ema_top,
    prefix = df_heights.columns[3])

df_ema_bottom = indicator.ema(
    df_in=df_heights,
    id='id',
    data=df_heights.columns[4],
    n = len_ema_bottom,
    prefix = df_heights.columns[4])


'''---------------------------------------------------------------------
    SIGNALS
---------------------------------------------------------------------'''

def wix(top, bottom):
    ''' If the top wick ema crosses over the bottom wick ema, return a
    1 (long), if the top wick crosses under the bottom wick ema, return
    a -1(short), otherwise return a 0 (do nothing)
    '''

    df_cross = cross.df_x_df(
        df_in_1 = top,
        df_in_2 = bottom,
        col_1 = top.columns[1],
        col_2 = bottom.columns[1])

    # Crossover
    if df_cross.iloc[-1, :][3]: signal = 1

    # Crossunder
    elif df_cross.iloc[-1, :][4]: signal = -1

    # No crossing
    else: signal = 0

    return signal





# // Overheated
# overbought = df_rsi > 92
# oversold = df_rsi < 32

# euphoria = ema_wick_top > ema_wick_top[1]*1.34 and ema_wick_top > ema_wick_top[2]*1.34
# dystopia = ema_wick_bottom > ema_wick_bottom[1]*1.3 and ema_wick_bottom > ema_wick_bottom[2]*1.2


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''
pass


'''
------------------------------------------------------------------------
    FUNCTIONS
------------------------------------------------------------------------
'''

'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    signal = wick(top = df_ema_top, bottom = df_ema_bottom)
