'''
------------------------------------------------------------------------
    EXCHANGE.PY
------------------------------------------------------------------------
Interface layer for the 'exchange' table in the database and exchange
related operations such as fetching data from the reading and writing
data from the exchanges, executing orders, getting balances etc
------------------------------------------------------------------------
'''

'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard library imports
import json
import os

# Third party imports
import pandas as pd
import ccxt

# Local application imports
from ccat.model.database.client import Client

'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Exchange():

    def __init__(self, exchange_id):

        self.id = exchange_id

        sql = f'SELECT * FROM exchange WHERE id = {self.id}'
        df = pd.read_sql(sql=sql, con = Client.get())

        self.name = df.name[0]
        self.api_key = os.environ[df.api_key[0]]
        self.api_secret = os.environ[df.api_secret[0]]

    def client(self):

        try:
            if self.id==3:
                self.client = ccxt.bitmex(
                    {'apiKey': self.api_key,
                    'secret': self.api_secret})

            ##### ADD MORE EXCHANGES HERE #####

            else:
                raise Exception('''\
                    CLIENT ERROR: Exchange not connected yet''')

        except Exception as e:
            print(e)
            raise e

        # Enable rate limiting to ensure we don't get locked out
        self.client.enableRateLimit = True

        return self.client
