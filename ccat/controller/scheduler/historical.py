'''
------------------------------------------------------------------------
    HISTORICAL.PY
------------------------------------------------------------------------
Populate the bucket table in the database with historical data

NOT READY

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
    '''Update the database with date from the given period'''

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

    # REPLACE
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


    # REPLACE
    # Dictionay of market_id's and their available timeframes. See above
    # Replace with a lookup in the database for valid timeframes
    # Get the timeframes in order from longest to shortest as the
    # shortest will naturally take longer to finalize and block all the
    # others
    instruments = {1:(6,4,2,1)}

    # Set up logging
    logging.basicConfig(
        filename=cf.lf_bucket_historical,
        level=logging.INFO)

    # Set number of periods to look back each time
    count = 500

    # Set the final end-date
    dt_stop = dt(2016, 1, 1)
    ts_stop = dt_stop.timestamp() * 1000

    # For each of the markets
    for market_id, timeframe_ids in instruments.items():

        # For each of the timeframes
        for timeframe_id in timeframe_ids:

            # Set inital end-date for each cycle
            ts_last = cf.now() # dt.now().timestamp()*1000
            dt_last = dt.utcfromtimestamp(ts_last/1000)

            while ts_last > ts_stop:

                # Milisecond length for the timeframe
                timeframe_ms = durations[timeframe_id]

                # Set time_begin for the log
                ts_first = ts_last - (count * timeframe_ms)
                dt_first = dt.utcfromtimestamp(ts_first/1000)

                # Set the current time for the log
                ts_now = cf.now() # dt.now().timestamp()*1000
                dt_now = dt.utcnow()


                try:
                    # Do the update for the given market and timeframe
                    update(
                        market_id = market_id,
                        timeframe_id = timeframe_id,
                        time_end = ts_last,
                        count = count)

                    # Log the event
                    msg = (
                        'host: {}, '
                        'db: {}, '
                        'market_id: {}, '
                        'timeframe_id: {}, '
                        'timeframe_ms: {}, '
                        'time_first: {} - {}, '
                        'time_last: {} - {}, '
                        'time_now: {} - {}')

                    logging.info(msg.format(
                            cf.db_host,
                            cf.db_name,
                            market_id,
                            timeframe_id,
                            timeframe_ms,
                            ts_first,
                            dt_first,
                            ts_last,
                            dt_last,
                            ts_now,
                            dt_now))

                    # Set timestamp of last candle to timestamp of first
                    # candle of the last round
                    ts_last = ts_first + 10 * timeframe_ms
                    dt_last = dt.utcfromtimestamp(ts_last / 1000)

                except:
                    e = sys.exc_info()[0]
                    logging.error(e)
                    continue

            # Sleep one second to avoid getting rate limited
            time.sleep(1)
