# IMPORTS --------------------------------------------------------------

import pdb

# Third party imports
import pandas as pd

# Local application imports
from ccat.model.database.client import Client


# MODULE ---------------------------------------------------------------

class Instrument():
    '''I/O interface layer for the 'instrument' table in the database.
    '''

    def __init__(self, market_id=1):

        self.market_id = market_id

        # Create first bit of the sql string
        sql=f'SELECT * FROM instrument WHERE market_id={self.market_id}'

        instrument = pd.read_sql(sql=sql, con=Client.get())

        # Set attributes of the order object from the instrument data

        self.market_symbol_native = instrument.market_symbol_native[0]
        self.market_symbol_ccxt = instrument.market_symbol_ccxt[0]
        self.market_description = instrument.market_description[0]

        self.pair_id = instrument.pair_id[0]

        self.asset_base_id = instrument.asset_base_id[0]
        self.asset_base_ticker = instrument.asset_base_ticker[0]
        self.asset_base_name = instrument.asset_base_name[0]
        self.asset_quote_id = instrument.asset_quote_id[0]
        self.asset_quote_ticker = instrument.asset_quote_ticker[0]
        self.asset_quote_name = instrument.asset_quote_name[0]

        self.exchange_id = instrument.exchange_id[0]
        self.exchange_name = instrument.exchange_name[0]
        self.exchange_api_key = instrument.exchange_api_key [0]
        self.exchange_api_secret = instrument.exchange_api_secret[0]

    def get(self):
        return self

