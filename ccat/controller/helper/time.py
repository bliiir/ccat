# IMPORTS --------------------------------------------------------------

# Standard library imports
import pdb

# import time
from datetime import datetime as dt
from datetime import timedelta as td
from dateutil.relativedelta import relativedelta as rd
from math import floor
import time

# Third party packages
import pandas as pd

# Local packages
pass

# MODULE ---------------------------------------------------------------


# Duration
minute = 60000
hour = minute * 60
day = hour * 24
week = day * 7


# # Present
now = floor((dt.utcnow().timestamp())*1000)

# # Past
hour_ago = floor(((dt.utcnow() - rd(hours=1)).timestamp())*1000)
day_ago = floor(((dt.utcnow() - rd(days=1)).timestamp())*1000)
week_ago = floor(((dt.utcnow() - rd(weeks=1)).timestamp())*1000)
month_ago = floor(((dt.utcnow() - rd(months=1)).timestamp())*1000)
year_ago = floor(((dt.utcnow() - rd(years=1)).timestamp())*1000)


# Convert epoch to datetime
def unix_to_datetime(
    df:pd.DataFrame,
    col:str = 'time_close'):

    col_new = f'{col}_ISO'

    df = df[['id', col]].copy()

    df[col_new] = pd.to_datetime(df[col], unit='ms')

    return df[['id', col_new]]