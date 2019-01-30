'''
------------------------------------------------------------------------
    BUCKET.PY
------------------------------------------------------------------------

I/O interface layer for the 'bucket' table in the database.
'''


'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard library imports
# import pdb

# Third party imports
import pandas as pd


# Local application imports
from ccat import config

from ccat.model.database.market import Market
from ccat.model.database.timeframe import Timeframe
from ccat.model.database.client import Client

from ccat.model.exchange.exchange import Exchange



'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Bucket():
    '''(C)RU(D) operations on the bucket table in the postgres database
    '''

    '''-----------------------------------------------------------------
    CREATE
    -----------------------------------------------------------------'''
    def __init__(self, market_id, timeframe_id):

        # Set instance attributes
        self.market_id = market_id
        self.timeframe_id = timeframe_id

        # Get market attributes from market table
        market = Market(self.market_id).get()

        self.market_symbol_native = market.symbol_native
        self.market_symbol_ccxt = market.symbol_ccxt
        self.market_description = market.description
        self.exchange_id = market.exchange_id
        self.pair_id = market.pair_id

        # Get timeframe attributes from timeframe table
        timeframe = Timeframe(self.timeframe_id)

        self.timeframe_name = timeframe.name
        self.timeframe_ms = timeframe.ms

        # Get a database client
        self.db_client = Client.get()


    '''-----------------------------------------------------------------
    READ
    -----------------------------------------------------------------'''

    # Execute the read query
    def read_execute(self, query, sort_col, sort_dir):

        #self.update() ###### REMOVE WHEN SUPERVISORD OR CRONJOB

        # Execute the query and store it in a pandas dataframe
        df_buckets = pd.read_sql(sql=query, con=self.db_client)

        # Sort by sort_col and direction
        df_buckets = df_buckets.sort_values(by=[sort_col],
                                            ascending=sort_dir=='ASC')
        df_buckets.set_index('id')
        return df_buckets


    def read_all(
        self,
        sort_col:str = 'time_close',
        sort_dir:str = 'ASC'):

        query = f'\
            SELECT * \
            FROM bucket \
            WHERE market_id = {self.market_id} \
            AND timeframe_id = {self.timeframe_id} \
            ORDER BY time_close ASC'

        return self.read_execute(query, sort_col, sort_dir)


    def read_between(
        self,
        time_begin: int = config.month_ago(),
        time_end: int = config.now(),
        sort_col: str = 'time_close',
        sort_dir: str = 'ASC'):

        query = f'\
            SELECT * \
            FROM bucket \
            WHERE market_id = {self.market_id} \
            AND timeframe_id = {self.timeframe_id} \
            AND time_open >= {time_begin} \
            AND time_close <= {time_end} \
            ORDER BY time_close ASC'

        return self.read_execute(query, sort_col, sort_dir)


    def read_latest(
        self,
        count=100,
        sort_col:str = 'time_close',
        sort_dir:str = 'ASC'):

        query = f'\
            SELECT * \
            FROM bucket \
            WHERE market_id = {self.market_id} \
            AND timeframe_id = {self.timeframe_id} \
            ORDER BY time_close ASC \
            LIMIT {count}'

        return self.read_execute(query, sort_col, sort_dir)


    def read_from(
        self,
        time_begin=config.month_ago(),
        count=100,
        sort_col:str = 'time_close',
        sort_dir:str = 'ASC'):

        query = f'\
            SELECT * \
            FROM bucket \
            WHERE market_id = {self.market_id} \
            AND timeframe_id = {self.timeframe_id} \
            AND time_open >= {time_begin} \
            ORDER BY time_close ASC \
            LIMIT {count}'

        return self.read_execute(query, sort_col, sort_dir)


    def read_until(
        self,
        time_end= config.now(),
        count=100,
        sort_col:str = 'time_close',
        sort_dir:str = 'ASC'):

        query = f'\
            SELECT * \
            FROM bucket \
            WHERE market_id = {self.market_id} \
            AND timeframe_id = {self.timeframe_id} \
            AND time_close <= {time_end} \
            ORDER BY time_close ASC \
            LIMIT {count}'

        return self.read_execute(query, sort_col, sort_dir)



    '''-----------------------------------------------------------------
    UPDATE
    -----------------------------------------------------------------'''

    def update(self, count=100, time_end=config.now(), time_begin=None):
            '''Get candles for the specified pair, timeframe from the
            specified exchange'''

            if time_begin == None:
                # Set the start of the date range to the end
                time_begin = time_end-(self.timeframe_ms * count)

            # Load the market info
            market = Market(market_id=self.market_id)
            exchange_id = market.get_exchange_id()

            # Get exchange instance
            exchange = Exchange(exchange_id = exchange_id)

            # Get an exchange client
            exchange_client = exchange.client()


            # Fetch the OHLCV data from the exchange
            self.buckets = exchange_client.fetch_ohlcv(
                symbol= self.market_symbol_ccxt,
                timeframe= self.timeframe_name,
                limit=count,
                since=time_begin)

            # Name the columns to comply with the database
            columns = [
                'time_close',
                'price_open',
                'price_high',
                'price_low',
                'price_close',
                'volume']

            # Store the results in a dataframe
            self.df_buckets=pd.DataFrame(self.buckets, columns=columns)

            # Add derived extra columns
            self.df_buckets['market_id'] = self.market_id
            self.df_buckets['timeframe_id'] = self.timeframe_id
            self.df_buckets['time_updated'] = config.now()
            self.df_buckets['time_open']=(self.df_buckets['time_close']
                                        - self.timeframe_ms)

            # Create 'temp_bucket' postgres database table with new data
            self.df_buckets.to_sql('bucket_temp', con=self.db_client,
                                    if_exists="replace")

            # Insert the df_buckets dataframe into the bucket table
            # ngn.DB.execute()

            # Create a temporary table
            # write data to the table
            # Drop the temporary table

            # Merge the 'bucket_temp' with the 'bucket' postgres table
            sql = '''
                INSERT INTO bucket(
                    market_id,
                    timeframe_id,
                    time_open,
                    time_close,
                    time_updated,
                    price_open,
                    price_high,
                    price_low,
                    price_close,
                    volume)
                SELECT
                    market_id,
                    timeframe_id,
                    time_open,
                    time_close,
                    time_updated,
                    price_open,
                    price_high,
                    price_low,
                    price_close,
                    volume
                FROM bucket_temp
                ON CONFLICT (market_id, timeframe_id, time_close)
                    DO NOTHING;'''

            con = self.db_client.connect()
            con.execute(sql)

            return self.df_buckets


'''
------------------------------------------------------------------------
    UNITTEST
------------------------------------------------------------------------
'''
# https://docs.python.org/3.7/library/unittest.html#module-unittest

import unittest

class Test_Bucket(unittest.TestCase):

    def setUp(self):

        self.market_id = 1
        self.timeframe_id = 1

        self.bucket = Bucket(
            market_id=self.market_id,
            timeframe_id=self.timeframe_id)


    def test_bucket_instantiation(self):
        self.assertEqual(self.bucket.market_id, self.market_id)


    def test_bucket_update(self):
        self.buckets = self.bucket.update()
        print('UPDATE: ', self.buckets)
        self.assertIsNotNone(self.buckets)

    def test_bucket_update_length(self):
        self.buckets = self.bucket.update(count=25)
        print('LENGTH: ', self.buckets)
        self.assertEqual(len(self.buckets), 25)


    def test_bucket_read_all(self):
        self.all = self.bucket.read_all()
        print('READ ALL: ', self.all)
        self.assertIsNotNone(self.all)



'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()
    # pass
