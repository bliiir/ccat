# IMPORTS --------------------------------------------------------------

# Standard library imports
import json
import uuid

# Third party imports
import pandas as pd

# Local application imports
from ccat.model.database.market import Market
from ccat.model.exchange.exchange import Exchange


# CLASSES --------------------------------------------------------------

class Order():
    '''Generalized order class to interact with the exchanges
    '''

    def __init__(self, market_id=1):
        '''Set internal id
        '''

        self.market_id = market_id

        # Get the exchange_id and symbol_ccxt from the market_id
        self.market = Market(self.market_id).get()
        self.exchange_id = self.market.exchange_id
        self.symbol_ccxt =self.market.symbol_ccxt
        self.symbol_native =self.market.symbol_native

        # Get exchange client from market_id
        self.exchange_client = Exchange(exchange_id=self.exchange_id).client()

        self.order_id = None
        self.order_status = None
        self.order_price = None
        self.order_time_executed = None
        self.order_time_submitted = None


    # Set standard output
    def __str__(self):


                # "internal id":self.internal_id,
                # "internal timestamp":self.timestamp_created,

        try:
            out = {
                "market_id":self.market_id,
                "exchange_id":self.exchange_id,
                "symbol_native":self.symbol_native,
                "order_id":self.order_id,
                "order_status":self.order_status,
                "order_time_submitted":self.order_time_submitted,
                "order_time_executed":self.order_time_executed,
                "order_price":self.order_price,
                "symbol_ccxt":self.symbol_ccxt}

            return str(out)

        except Exception as e:
            error_message = 'Error: ' + str(e)
            return error_message


    # Set post-order-creation instance attributes
    def populate(self):
        self.order_id = self.order['info']['orderID']
        self.order_status = self.order['info']['ordStatus']
        self.order_price = self.order['info']['price']
        self.order_time_executed = self.order['info']['transactTime']
        self.order_time_submitted = self.order['info']['timestamp']

        return self


    # Load order from exchange by order_id or self.order_id
    def load(self, order_id = None):

        # Use order_id it is submitted or self.order_id if not
        if order_id != None: self.order_id = order_id

        # Get the order from the exchange
        self.order = self.exchange_client.fetch_order(id=self.order_id)

        # Update the object with the new info from the exchange
        self.populate()

        return self


    def submit(self, side, amount, order_type = 'market'):
        '''Submit a new order to the exchange.

        The default order type is a market order
        '''

        # Set pre-order-creation instance attributes
        self.order_side = side
        self.order_amount = amount,
        self.order_type = order_type

        # Place and load the order into self.order
        self.order = self.exchange_client.create_order(
            side=self.order_side,
            symbol=self.symbol_ccxt,
            type=self.order_type,
            amount=self.order_amount)

        # Populate the instance attributes from self.order
        self.populate()

        return self


    def cancel(self, order_id=None):
        '''Delete unfilled orders
        '''

        if order_id != None:
            self.order_id = order_id

        try:

            # Cancel the order
            self.order = self.exchange_client.cancel_order(id=self.order_id)

            # return the status
            return self.order['info']['ordStatus']

        except Exception as e:
            message = "ERROR: " + str(e)
            return message




