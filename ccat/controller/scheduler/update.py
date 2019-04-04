# IMPORTS --------------------------------------------------------------

# Standard library imports
pass

# Third party imports
pass

# Local application imports
from ccat import config as cf
from ccat import bucket

import bucket


# FUNCTIONS ------------------------------------------------------------

def update(
    market_id = 1, # Bitmex
    timeframe_id = 6,  # 1d
    time_end = cf.now(),
    count = 500):
    '''Update the database with date from the given period'''


    bucket.Bucket(
        market_id=market_id,
        timeframe_id=timeframe_id).update(count=count,
            time_end=time_end)


# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    import sys
    import time
    import logging
    from datetime import datetime as dt

    # Get arguments from the cronjob
    market_id = int(sys.argv[1])
    timeframe_id = int(sys.argv[2])
    count = int(sys.argv[3])

    # Do the update
    update(
        market_id = market_id,
        timeframe_id = timeframe_id,
        count=count)

    # Log the event
    logging.basicConfig(
        filename=cf.lf_bucket_update,
        level=logging.DEBUG)

    # Set the current time for the log
    utcnow = dt.utcnow()
    time_now = dt.strftime(utcnow, "%Y.%m.%d %H:%M:%S")

    loggin.info

    logging.info(f'\
        host: {cf.db_host}, \
        db: {cf.db_name}, \
        market_id: {market_id}, \
        timeframe_id: {timeframe_id}, \
        count: {count}, \
        time_now: {time_now} / {utcnow.timestamp()}')
