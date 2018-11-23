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
pass

# Third party imports
import pandas as pd
ccat
# Local application imports
from ccat.exchange import Exchange as ex
import ccat.config as cf
from ccat.engine import SqlEngine as ngn

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

        # Args
        self.market_id = market_id
        self.timeframe_id = timeframe_id


        # Get attributes from the instrument view
        sql = f'''SELECT * FROM instrument
                            WHERE market_id={self.market_id}'''

        self.df_instr = pd.read_sql(sql=sql, con=ngn.get())

        self.market_id = self.df_instr.market_id[0]
        self.market_symbol_native = self.df_instr.market_symbol_native[0]
        self.market_symbol_ccxt = self.df_instr.market_symbol_ccxt[0]
        self.market_description = self.df_instr.market_description[0]

        self.exchange_id = self.df_instr.exchange_id[0]
        self.exchange_name = self.df_instr.exchange_name[0]

        self.pair_id = self.df_instr.pair_id[0]

        self.asset_base_id = self.df_instr.asset_base_id[0]
        self.asset_base_ticker = self.df_instr.asset_base_ticker[0]
        self.asset_base_name = self.df_instr.asset_base_name[0]

        self.asset_quote_id = self.df_instr.asset_quote_id[0]
        self.asset_quote_ticker = self.df_instr.asset_quote_ticker[0]
        self.asset_quote_name = self.df_instr.asset_quote_name[0]


        # Get the attributes from the timeframe table
        sql = f'SELECT * FROM timeframe \
                WHERE id={self.timeframe_id}'

        self.df_timeframe = pd.read_sql(sql=sql, con=ngn.get())

        self.timeframe_name = self.df_timeframe.name[0]
        self.timeframe_ms = self.df_timeframe.milliseconds[0]


    '''-----------------------------------------------------------------
    READ
    -----------------------------------------------------------------'''

    # Execute the read query
    def read_execute(self, query, sort_col, sort_dir):

        # Execute the query and store it in a pandas dataframe
        df_buckets = pd.read_sql(sql=query, con=ngn.get())

        # Sort by sort_col and direction
        df_buckets = df_buckets.sort_values(by=[sort_col],
                                            ascending=sort_dir=='ASC')
        df_buckets.set_index('id')
        return df_buckets


    def read_all(
        self,
        sort_col:str = 'time_close',
        sort_dir:str = 'DESC'):

        query = f'\
            SELECT * \
            FROM bucket \
            WHERE market_id = {self.market_id} \
            AND timeframe_id = {self.timeframe_id} \
            ORDER BY time_close DESC'

        return self.read_execute(query, sort_col, sort_dir)


    def read_between(
        self,
        time_begin: int = cf.month_ago(),
        time_end: int = cf.now(),
        sort_col: str = 'time_close',
        sort_dir: str = 'DESC'):

        query = f'\
            SELECT * \
            FROM bucket \
            WHERE market_id = {self.market_id} \
            AND timeframe_id = {self.timeframe_id} \
            AND time_open >= {time_begin} \
            AND time_close <= {time_end} \
            ORDER BY time_close DESC'

        return self.read_execute(query, sort_col, sort_dir)


    def read_latest(
        self,
        count=100,
        sort_col:str = 'time_close',
        sort_dir:str = 'DESC'):

        query = f'\
            SELECT * \
            FROM bucket \
            WHERE market_id = {self.market_id} \
            AND timeframe_id = {self.timeframe_id} \
            ORDER BY time_close DESC \
            LIMIT {count}'

        return self.read_execute(query, sort_col, sort_dir)


    def read_from(
        self,
        time_begin=cf.month_ago(),
        count=100,
        sort_col:str = 'time_close',
        sort_dir:str = 'DESC'):

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
        time_end= cf.now(),
        count=100,
        sort_col:str = 'time_close',
        sort_dir:str = 'DESC'):

        query = f'\
            SELECT * \
            FROM bucket \
            WHERE market_id = {self.market_id} \
            AND timeframe_id = {self.timeframe_id} \
            AND time_close <= {time_end} \
            ORDER BY time_close DESC \
            LIMIT {count}'
        print(query)
        return self.read_execute(query, sort_col, sort_dir)



    '''-----------------------------------------------------------------
    UPDATE
    -----------------------------------------------------------------'''

    def update(self, count=100, time_end=cf.now()):
            '''Get candles for the specified pair, timeframe from the
            specified exchange'''

            # Set the start of the date range to the end
            time_begin = time_end-(self.timeframe_ms * count)

            # Get exchange client
            exchange = ex(self.exchange_id)
            client = exchange.client()

            # Fetch the OHLCV data from the exchange
            self.buckets = client.fetch_ohlcv(
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
            self.df_buckets['time_updated'] = cf.now()
            self.df_buckets['time_open']=(self.df_buckets['time_close']
                                        - self.timeframe_ms)

            # Create 'temp_bucket' postgres database table with new data
            self.df_buckets.to_sql('bucket_temp', con=ngn.get(),
                                    if_exists="replace")

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

            con = ngn.get().connect()
            con.execute(sql)

            return self.df_buckets


'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    # import time

    cp1 = cf.now()
    print('checkpoint: ', cp1)

    b = Bucket(market_id=1,timeframe_id=1)
    cp2 = cf.now()
    print('done creating the bucket')
    print('checkpoint: ', cp2, cp2-cp1)

    g = b.update()
    cp3 = cf.now()
    print('Done getting the data from the exchange')
    print('checkpoint: ', cp3, cp3-cp2)

    time.sleep(1)

    # r = b.read_between(count=50)
    # r = b.read_between(time_end=1542741540000, time_begin=1542740220000)
    r = b.read_all()
    cp4 = cf.now()
    print('Done reading from the database')
    print('checkpoint: ', cp3, cp4-cp3)
    print(r)



