# IMPORTS --------------------------------------------------------------

# Standard library imports
pass

# Third party imports
import pandas as pd

# Local application imports
# from ccat.model.database.client import Client
from ccat.model.database.client import Client


# MODULE --------------------------------------------------------------

class Market():
    '''I/O interface layer for the 'market' table in the database.
    '''

    def __init__(self, market_id=1):

        self.market_id = market_id

        sql = f'SELECT * FROM market WHERE id = {self.market_id}'
        df = pd.read_sql(sql=sql, con=Client.get())

        # Set attributes of the market object from the market table
        self.exchange_id = df.exchange_id[0]
        self.pair_id = df.pair_id[0]
        self.symbol_native = df.symbol_native[0]
        self.symbol_ccxt = df.symbol_ccxt[0]
        self.description = df.description[0]


    def get(self):
        return self

    def get_exchange_id(self):
        return self.exchange_id