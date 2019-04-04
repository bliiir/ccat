#!/usr/bin/env python
# coding: utf-8

# SIMULATION ---------------------------------------------------------------

# Strategy simulation

# Objective: Build a module that allows me to backtest my strategies


# CONFIG ---------------------------------------------------------------

# Standard imports
import datetime as dt
from dateutil.relativedelta import relativedelta as rd

# Third party imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

# local application imports
from ccat.model.database.bucket import Bucket
from ccat.controller.strategy.momentum import Momentum
from ccat.controller.helper import time as t
from ccat.controller.helper import df_magic


# CONFIG ---------------------------------------------------------------

### Configure Matplotlib
# get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('seaborn-whitegrid')
register_matplotlib_converters()

### Instrument
market_id = 1
timeframe_id = 6

### Time
time_begin_dt = dt.datetime(2017, 12, 1, 0, 0, 0)
time_end_dt = dt.datetime(2020, 2, 20, 0, 0, 0)

time_begin_unix = time_begin_dt.timestamp() * 1000
time_end_unix = time_end_dt.timestamp() * 1000

### Time calculations
elapsed_dt = time_end_dt - time_begin_dt

elapsed_seconds = elapsed_dt.total_seconds()
elapsed_minutes = elapsed_seconds/60
elapsed_hours = elapsed_minutes/60
elapsed_days = elapsed_hours/24
elapsed_weeks = elapsed_days/7
elapsed_months = elapsed_days/30
elapsed_years = elapsed_days/365


## Strategy specific

### Signals

#### Reversal
reversal_len_ma_top = 40
reversal_len_ma_bottom = 40
reversal_prefix = 'reversal'

#### Extreme
extreme_len_ma_top = 40
extreme_len_ma_bottom = 40
extreme_prefix = 'extreme'
extreme_l1 = 2
extreme_l2 = 2
extreme_s1 = 2
extreme_s2 = 2

# #### Overtraded
overtraded_len_rsi = 15
overtraded_high = 60
overtraded_low = 31
overtraded_col = 'price_close'
overtraded_prefix = 'overtraded'


# STRATEGY ---------------------------------------------------------------

# Get a bucket instance with the right market and timeframe id's
bucket = Bucket(market_id = market_id, timeframe_id = timeframe_id)

# Get timeframe duration in miliseconds
timeframe_ms = bucket.timeframe_ms

# Update table with the candles for the timeframe
bucket.update(time_begin = time_begin_unix, time_end = time_end_unix)
pass

# Get the dataframe with the bucket data between the begin and end dates
df_bucket = bucket.read_between(time_begin = time_begin_unix, time_end = time_end_unix)

# Create strategy instance using the configurations above
strategy = Momentum(

    df_bucket = df_bucket,

    reversal_len_ma_top = reversal_len_ma_top,
    reversal_len_ma_bottom = reversal_len_ma_bottom,
    reversal_prefix = reversal_prefix,

    extreme_len_ma_top = extreme_len_ma_top,
    extreme_len_ma_bottom = extreme_len_ma_bottom,
    extreme_prefix = extreme_prefix,
    extreme_l1 = extreme_l1,
    extreme_l2 = extreme_l2,
    extreme_s1 = extreme_s1,
    extreme_s2 = extreme_s2,

    overtraded_len_rsi = overtraded_len_rsi,
    overtraded_high = overtraded_high,
    overtraded_low = overtraded_low,
    overtraded_col = overtraded_col,
    overtraded_prefix = overtraded_prefix)


# Add the strategy indicators and signals as columns to the dataframe
df = strategy.all()


# SIMULATION ---------------------------------------------------------------

# Ignore chained assignment warning
pd.options.mode.chained_assignment = None

# Simulation column
col = 'reversal_signal'

# Make a copy of the strategy dataframe for the simulation
df_sim = df.copy()

# Initial capital
base = [0]
quote = [1000]

stake_size = 1
fee_size = 0.00075
slippage_size = 0.0001


for i in range(1, len(df_sim)):

    # Set previous holdings
    base_prev = base[i-1]
    quote_prev = quote[i-1]

    #
    price_open = df_sim['price_open'].values[i]
    signal = df_sim[col].values[i]

    stake_quote = quote_prev * stake_size
    stake_base = base_prev * stake_size

    # Long
    if signal >= 1:
        base_delta = stake_quote / price_open
        quote_delta = -stake_quote

    # Short
    elif signal <= -1:
        base_delta = - stake_base
        quote_delta = stake_base * price_open

    # Hold
    else:
        base_delta = 0
        quote_delta = 0


    base_new = base_prev + base_delta
    quote_new = quote_prev + quote_delta

    base.append(base_new)
    quote.append(quote_new)


df_sim['base'] = base
df_sim['quote'] = quote
df_sim['value_quote'] = df_sim['quote'] + df_sim['base'] * df_sim['price_open']
df_sim['value_base'] = df_sim['base'] + df_sim['quote'] / df_sim['price_open']
df_sim['value_total'] = df_sim['value_quote'] + df_sim['value_base']

# Extreme
cols = []

fig1 = plt.figure(figsize = (25,10))
ax1 = plt.subplot(4, 1, 1)
ax2 = plt.subplot(4, 1, 2, sharex = ax1)
ax3 = plt.subplot(4, 1, 3, sharex = ax1)

# fig2 = plt.figure(figsize = (25,10))
ax4 = plt.subplot(4, 1, 4, sharex = ax1)

ax1.plot(df_sim['time_close_ISO'], df_sim['price_open'], color='b')
ax1.plot(df_sim['time_close_ISO'], df_sim['price_high'], alpha = 0.5)
ax1.plot(df_sim['time_close_ISO'], df_sim['price_low'], alpha = 0.5)
ax1.plot(df_sim['time_close_ISO'], df_sim['price_close'], alpha = 0.5)

ax2.plot(df_sim['time_close_ISO'], df_sim['value_quote'], color='pink')
ax2.plot(df_sim['   time_close_ISO'], df_sim['value_base'], color='orange')
# ax2.plot(df_sim['time_close_ISO'], df_sim['value_total'], color='green')

ax4.plot(df_sim['time_close_ISO'], df_sim['reversal_abs_top_40_ema'], color='b')  # extreme_abs_top_40_ema
ax4.plot(df_sim['time_close_ISO'], df_sim['reversal_abs_bottom_40_ema'], color='r')  # extreme_abs_top_40_ema

# ax2.plot(df['time_close_ISO'], df.iloc[:,30], color='r')  # extreme_abs_bottom_40_ema

ax3.plot(df_sim['time_close_ISO'], df_sim['reversal_signal'] , color='r')
# ax2.plot(df['time_close_ISO'], df['overtraded_long'], color='g')

plt.show()


