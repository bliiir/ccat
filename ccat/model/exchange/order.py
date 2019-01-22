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
import uuid

# Third party imports
import pandas as pd

# Local application imports
from ccat import config
from ccat.model.database.market import Market
from ccat.model.exchange.exchange import Exchange


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Order():
    '''Generalized order class to interact with the exchanges
    '''

    def __init__(self):
        '''Set internal id
        '''
        self.internal_id = uuid.uuid4()
        self.timestamp_created = config.now()

    def __str__(self):
        pass

    # Set post-order-creation instance attributes
    def populate(self):
        self.order_id = self.order['info']['orderID']
        self.order_status = self.order['info']['ordStatus']
        self.order_price = self.order['info']['price']
        self.order_time_executed = self.order['info']['transactTime']
        self.order_time_subimtted = self.order['info']['timestamp']


    # def get_symbol_ccxt(self):
    #     pass


    # Load order from exchange by order_id or self.order_id
    def load(self, order_id = None):

        # Use order_id it is submitted or self.order_id if not
        if order_id != None: self.order_id = order_id

        # Get the order from the exchange
        self.order = self.exchange_client.fetch_order(id=self.order_id)

        # Update the object with the new info from the exchange
        self.populate()


    def submit(
        self,
        side,
        amount,
        order_type='market',
        market_id=1):
        '''Submit a new order to the exchange
        '''

        # Set pre-order-creation instance attributes
        self.order_side = side
        self.order_amount = amount,
        self.order_type = order_type
        self.market_id = market_id

        # Get the exchange_id from the market_id
        self.market = Market(self.market_id).get()
        self.exchange_id = self.market.exchange_id
        self.symbol_ccxt =self.market.symbol_ccxt
        self.symbol_native =self.market.symbol_native

        # Get exchange client from market_id
        self.exchange = Exchange(exchange_id=self.exchange_id)
        self.exchange_client = self.exchange.client()

        # Place and load the order
        self.order = self.exchange_client.create_order(
            side=self.order_side,
            symbol=self.symbol_ccxt,
            type=self.order_type,
            amount=self.order_amount,
            )

        self.populate()

        return self


    def delete(self, order_id=None):
        '''Delete unfilled orders

        Check the order status - if it does not say 'open', then return
        an error message with the status.

        Possible responses: 'open', 'closed', 'cancelled', 'rejected', 'filled'.
        See more detail under parse_order_status here:
        https://github.com/ccxt/ccxt/blob/master/python/ccxt/bitmex.py
        '''

        if order_id != None:
            self.order_id = order_id

        # Load the order from the exchange
        self.load()

        # Return the order status if the order status on the exchange
        # isn't 'open'
        if self.order_status != open:
            return self.order_status

        else:
            self.order = self.exchange_client.cancel_order(id=self.order_id)
            self.load()
            return self.order_status


'''
------------------------------------------------------------------------
    UNITTEST
------------------------------------------------------------------------
'''

import unittest

class Test_order(unittest.TestCase):

    # Setup
    def setUp(self):
        self.my_order = Order()

        self.status_options =  [
            'canceled',
            'open',
            'closed',
            'new',
            'partiallyfilled',
            'filled',
            'doneforday',
            'canceled',
            'pendingcancel',
            'pendingnew',
            'rejected',
            'expired',
            'stopped',
            'untriggered',
            'triggered']

    # def test_order_not_none(self):
    #     print("\nORDER ID: ", self.my_order.internal_id)
    #     self.assertIsNotNone(self.my_order)

    # def test_order_id(self):
    #     print('\nLENGTH: ', len(str(self.my_order.internal_id)))
    #     self.assertEqual(len(str(self.my_order.internal_id)), 36)

    # def test_load_from_id(self):
    #     pass

    # def test_submit(self):
    #     order = self.my_order.submit(
    #         side = 'sell',
    #         amount = 1,
    #         order_type ='market',
    #         market_id = 1)
    #     print('STATUS: ', order.order_status)
    #     print('ORDER ID: ', order.order_id)
    #     self.assertIn(order.order_status.lower(), self.status_options)


    def test_load(self):
        order = self.my_order.load(order_id = '8a26a525-c6e6-f284-754c-7ebcf221ac7a')
        print('STATUS: ', order.order_status)
        print('ORDER ID: ', order.order_id)
        self.assertIn(order.order_status.lower(), self.status_options)


    # # Ways of making an order instance
    # def test_submit_new_order_to_exchange(self):

    #     self.my_order.submit(
    #         side='sell',
    #         amount=1,
    #         order_type='market',
    #         market_id=1)

    #     self.assertIsNotNone(self.my_order)

    # def test_load_existing_order_from_exchange_via_self(self):
    #     pass

    # # Ways of getting an order's status
    # def test_load_existing_order_from_exchange_via_order_id(self):
    #     pass

    # def test_update_existing_order_status_from_order_id(self):
    #     pass

    # def test_delete_order_via_self(self):
    #     pass

    # def test_delete_order_via_order_id(self):
    #     pass



'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''


if __name__ == '__main__':

    unittest.main()








