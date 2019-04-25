# IMPORTS --------------------------------------------------------------

# Standard imports
import pdb
import logging

import sys
from datetime import datetime as dt

# Third party imports
pass

# local application imports
from ccat import config
from ccat.model.database.bucket import Bucket
from ccat.model.exchange.order import Order
from ccat.controller.strategy.reversal import Strategy


# SETTINGS -------------------------------------------------------------

# Get arguments from the cronjob/terminal.
# Default to default settings if sys.argv does not have any arguments
try:
    '''
    Cronjob:
    0 0 * * * python3 bot.py 1 6 500 10

    Run bot.py with the arguments below every day at midnight:
    sys.argv[1] = 1     > market_id = 1
    sys.argv[2] = 6     > timeframe_id = 6
    sys.argv[3] = 500   > count = 500
    sys.argv[4] = 500   > stake_size = 500
    '''
    market_id = int(sys.argv[1])
    timeframe_id = int(sys.argv[2])
    count = int(sys.argv[3])
    stake_size = int(sys.argv[4])

# If no ill-formed arguments are passed, a test order is created
# TODO: Remove this hack and pass args to sys.argv instead
except:
    market_id = 1
    timeframe_id = 6
    count = 500
    stake_size = 1

# Strategy settings
kwargs = {
    'len_ma_top': 24, #24
    'len_ma_bottom': 24,
    'prefix':'reversal'}


# EXECUTE STRATEGY -----------------------------------------------------

# Get a bucket instance with the right market and timeframe id's
bucket = Bucket(market_id = market_id, timeframe_id = timeframe_id)

# Update table with the candles for the timeframe
bucket.update(count=count)

# Get the dataframe with the bucket data for the latest count candles
df_bucket = bucket.read_latest(count=count)

# Create strategy instance using the strategy settings
strategy = Strategy(df_bucket = df_bucket, **kwargs)

# Get signal
signal = strategy.signal()


# LOGGING --------------------------------------------------------------

logging.basicConfig(
    filename=config.lf_bot,
    level=logging.INFO)


def do_log(order):
    info = (
        '{:3} | '
        'utc: {:<20} | '
        'signal: {:2} | '
        'stake: {:6} | '
        'status: {:<9} | '
        'timeframe_id: {:1} | '
        'market_id: {:3} | ').format(
            '',
            dt.strftime(dt.utcnow(), "%Y.%m.%d %H:%M:%S"),
            signal,
            stake_size,
            order.order_status,
            timeframe_id,
            market_id)
    logging.info(info)



# EXECUTE ORDER --------------------------------------------------------

def execute(signal):

    if signal != 0:
        order = Order(market_id = market_id)

        if signal == 1:
            order = order.submit(side = 'buy', amount = stake_size)
            do_log(order)
            return order

        elif signal == -1:
            order = order.submit(side = 'sell', amount = stake_size)
            do_log(order)
            return order

    else:
        order = type('Order', (object,), {})()
        order.order_status = "-"
        do_log(order)
        return order


# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    execute(signal)