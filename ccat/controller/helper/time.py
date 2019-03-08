'''
------------------------------------------------------------------------- - - -
    IMPORTS
------------------------------------------------------------------------- - - -
'''

# Standard library imports
# import time
from datetime import datetime as dt
from datetime import timedelta as td
from dateutil.relativedelta import relativedelta as rd
from math import floor

# Third party packages
pass

# Local packages
pass

'''
------------------------------------------------------------------------- - - -
    IMPORTS
------------------------------------------------------------------------- - - -
'''

# Duration
minute = 60000
hour = minute * 60
day = hour * 24
week = day * 7

# # Present
now = floor((dt.now().timestamp())*1000)

# # Past
hour_ago = floor(((dt.now() - rd(hours=1)).timestamp())*1000)
day_ago = floor(((dt.now() - rd(days=1)).timestamp())*1000)
week_ago = floor(((dt.now() - rd(weeks=1)).timestamp())*1000)
month_ago = floor(((dt.now() - rd(months=1)).timestamp())*1000)
year_ago = floor(((dt.now() - rd(years=1)).timestamp())*1000)