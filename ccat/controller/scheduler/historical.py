'''
------------------------------------------------------------------------
    HISTORICAL.PY
------------------------------------------------------------------------
Populate the bucket table in the database with historical data
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

# Local application imports
from ccat import engine as ngn
from ccat import config as cf
from ccat import bucket


'''
------------------------------------------------------------------------
    FUNCTIONS
------------------------------------------------------------------------
'''

def update(
    market_id = 1, # Bitmex
    timeframe_id = 6,  # 1d
    time_end = cf.now(),
    count = 500):

    bucket.Bucket(
        market_id=market_id,
        timeframe_id=timeframe_id).update(count=count, time_end=time_end)

'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    import sys
    import time
    import logging

    from datetime import datetime as dt
    from math import floor


    # This section should be replaced with a lookup in the database
    # joining the exchange associated with the market_id with the
    # timeframes available for that exchange
    durations = {
        1:60000, # 1m
        2:300000, # 5m
        3:900000, # 15m
        4:3600000, # 1h
        5:14400000, # 4h
        6:86400000, # 1d
        7:604800000, # 7d
        8:2592000000 # 30d
        }

    # Dictionay of market_id's and their available timeframes. See above
    instruments = {1:(1,2,4,6)}

    # Set up logging
    logging.basicConfig(filename=cf.lf_bucket_historical, level=logging.DEBUG)

    # Set number of periods to look back each time
    count = 500

    # Set starting end-date
    time_end = cf.now()

    # Do until we have all the candles available
    while True:

        # For each of the markets
        for market_id, timeframe_ids in instruments.items():

            # For each of the timeframes
            for timeframe_id in timeframe_ids:

                # Milisecond length for the timeframe
                timeframe_ms = durations[timeframe_id]

                # Set time_begin for the log
                time_begin = time_end - count * timeframe_ms

                # Set the current time for the log
                time_now = dt.strftime(dt.now(), "%Y.%M.%d %H:%M:%S")

                # Do the update for the given market and timeframe
                # update(
                #     market_id = market_id,
                #     timeframe_id = timeframe_id,
                #     time_end = time_end,
                #     count = count)

                # Log the event
                logging.info(f'\
                    host: {cf.db_host},\
                    db: {cf.db_name},\
                    market_id: {market_id},\
                    timeframe_id: {timeframe_id},\
                    time_end: {time_end},\
                    time_begin: {time_begin},\
                    time_now: {time_now} \n')


        # Set end date to the begin date plus ten candles
        time_end = time_begin + 10 * timeframe_ms

        # I guess this should really be terminated in the code, but I will try to let it run and see what happens
