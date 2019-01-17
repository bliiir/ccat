'''
------------------------------------------------------------------------
    ORDER.PY
------------------------------------------------------------------------
Place, update and get info about an order on an exchange
'''


'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard library imports
import json

# Third party imports
import pandas as pd

# Local application imports
from ccat import config
from ccat import exchange
from ccat import engine


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Order(): # Rename to Bitmex?
    '''Order objects contain order info, status and update methods.
    '''

    # Assemble the __str__ string
    def __str__(self):
        return f'\ntype: {type(self)},\n\n methods: {dir(self)},\n\n variables: {vars(self)}'


    # Create and submit the order
    def create_order(
        self,
        side:str,
        market_id: int = 1,
        order_type:str = 'Market',
        amount:float = 0,
        trigger:float = None,
        limit:float = None):
        '''Create an order

        Args:

        :market_id (int):
            The market id as it is found in the database

        :side (str):
            The side of the order. Possible values are:
                'buy',
                'sell',

        :order_type (str):
            The order type. Possible values are:
                'market',

        :trigger (float), optional:
            The trigger price. Only relevant for stop_loss or
            take-profit orders.

        :limit (float), optional:
            The limit price.
            If == None, the order is submitted as a market order
            If != None the order is submitted as a limit order.


        See https://github.com/ccxt/ccxt/wiki/Manual#placing-orders
        '''

        # We know that we are getting a market_id, so lets populate the
        # order with what we have based on that
        self.market_id = market_id

        # Use the instrument view in the database with the market_id
        sql = f'SELECT * FROM instrument \
            WHERE market_id={self.market_id}'

        df_instrument = pd.read_sql(sql=sql, con=engine.Db.get())

        # Set attributes of the order object from the instrument data
        self.exchange_id = df_instrument.exchange_id[0]
        self.symbol_ccxt = df_instrument.market_symbol_ccxt[0]

        # Get exchange client
        self.exchange = exchange.Exchange(self.exchange_id)
        self.exchange_client = self.exchange.client()

        # This we don't really need
        # self.exchange_name = df_instrument.exchange_name[0]
        # self.asset_base_id = df_instrument.asset_base_id[0]
        # self.asset_base_ticker = df_instrument.asset_base_ticker[0]
        # self.asset_base_name = df_instrument.asset_base_name[0]
        # self.asset_quote_id = df_instrument.asset_quote_id[0]
        # self.asset_quote_ticker = df_instrument.asset_quote_ticker[0]
        # self.asset_quote_name = df_instrument.asset_quote_name[0]
        # self.pair_id = df_instrument.pair_id[0]

        self.side = side
        self.order_type = order_type
        self.amount = amount,
        # self.trigger = trigger
        # self.limit = limit

        self.order = self.exchange_client.create_order(
            side=self.side,
            symbol=self.symbol_ccxt,
            type=self.order_type,
            amount=self.amount)

        self.order_id = self.order['info']['orderID']
        # self.order_status = self.order['info']['ordStatus']
        # self.order_price = self.order['info']['price']
        # self.order_time_executed = self.order['info']['transactTime']
        # self.order_time_subimtted = self.order['info']['timestamp']

        return self.order


    # Return order info from object
    def read_order(self, order_id: str = None, order = None):

        # If we are recieving an order id, we can fetch the order info
        # from the exchange
        if order_id != None:
            self.order_id = order_id
            self.order = self.exchange_client.fetch_order(id=self.order_id)

        # If we are getting an order object, we can set this instance to
        # that object and retrieve the order_id from that
        elif order != None:
            self.order = order
            self.order_id = self.order['info']['orderID']

        else:
            self.order = None
            self.order_id = None

        try:
            return self.order
        except:
            return 'no order yet. Try to create() one first. Have a lovely day!'

        if self.order == None:
            pass

    # Get the order_id
    def get_order_id(self):
        return self.order_id


    # Update the object with info from the exchange
    def update_order(self):
        self.order = self.exchange_client.fetch_order(id=self.order_id)
        return self.order

    def delete_order():
        '''Delete unfilled orders

        Check the order status - if it does not say 'open', then return
        an error message with the status.

        Possible responses: 'open', 'closed', 'cancelled', 'rejected'.
        See more detail under parse_order_status here:
        https://github.com/ccxt/ccxt/blob/master/python/ccxt/bitmex.py
        '''
        self.order = self.exchange_client.cancel_order(id=self.order_id)
        return self.order


'''
------------------------------------------------------------------------
    UNITTEST
------------------------------------------------------------------------
'''


# import unittest

# class Test_order(unittest.TestCase)


'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''


if __name__ == '__main__':

    import json

    # unittest.main()

    # order1 = Order(market_id = 1, order_id='9fbad803-52d8-be14-e138-1964ba87f429')
    # order2 = Order(market_id = 1, order=order1.read_order())
    order3 = Order()
    order3.create_order(side = 'Sell', market_id = 1, amount = 1)
    order3_id = order3.get_order_id()

    # print('order: ', order1)
    # print('order: ', order2)
    print('order3_id: ', order3_id)

    # print('create: ', order.create_order(side = 'Sell', amount = 1))

    # print('read: ', json.dumps(order.read_order(), indent=4))

    # print('update: ', order.update_order())

    # print('delete: ' order.delete_order())








