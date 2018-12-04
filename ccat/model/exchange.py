'''
------------------------------------------------------------------------- - - -
Interface layer for the 'exchange' table in the database and exchange
related operations such as fetching data from the reading and writing
data from the exchanges, executing orders, getting balances etc
------------------------------------------------------------------------- - - -
'''

'''
------------------------------------------------------------------------- - - -
    IMPORTS
------------------------------------------------------------------------- - - -
'''

# Standard library imports
import json

# Third party imports
import pandas as pd
import ccxt
import psycopg2

# Local application imports
from ccat import engine as ngn

'''
------------------------------------------------------------------------- - - -
    CLASSES
------------------------------------------------------------------------- - - -
'''

class Exchange():

    def __init__(self, exchange_id):
        '''Create an exchange instance here from the exchange id that pulls
        the id, name, api key and secret from the cf.db_name/the environment
        '''

        self.id = exchange_id

        '''Read exchange data from the database'''
        query = f'SELECT * FROM exchange WHERE id={self.id}'
        df = pd.read_sql(sql=query, con=ngn.Db.get())

        # Set the instance variables
        self.name = df.name
        self.api_key = df.api_key
        self.api_secret = df.api_secret


    # Create an exchange client for the exchange corresponding to the exchange_id
    def client(self):
        '''Create the client'''

        try:
            if self.id==3:
                self.client = ccxt.bitmex({'apiKey': self.api_key, 'secret': self.api_secret})
                return self.client

            ##### ADD MORE EXCHANGES HERE #####

            else:
                raise Exception('CLIENT ERROR: Exchange not registered in the system')

        except Exception as e:
            print(e)
            raise e


'''
------------------------------------------------------------------------- - - -
    UNIT TEST
------------------------------------------------------------------------- - - -
'''

# Run if executed directly. Do not run it if import
if __name__ == '__main__':

    # Testing the functionality - MOVE TO UNIT TEST
    e = Exchange(3)
    bitmex = e.client()

    # Fetch the 1h BTC candles
    candles = bitmex.fetchOHLCV('BTC/USD', '1h', limit=100, since=bitmex.parse8601 ('2018-11-5T00:00:00Z'))

    df = pd.DataFrame(candles)
    df.columns = ['time_close', 'price_open', 'price_high', 'price_low', 'price_close', 'volume' ]
    print(df.tail(10))



