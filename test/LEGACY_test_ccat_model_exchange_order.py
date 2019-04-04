'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest

# Third party packages
pass

# Local packages
from ccat.model.exchange.order import Order


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''


class Test_model_exchange_order(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.my_order = Order(market_id=1)

        # self.test_id = '8a26a525-c6e6-f284-754c-7ebcf221ac7a'
        cls.test_id = '52b43253-03de-9cb8-7664-eaa6dae51d7e'

        cls.status_options = [
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


    def test_str_(self):
        self.assertIn("order_status", self.my_order.__str__())


    def test_order_not_none(self):
        # print("\nORDER ID: ", self.my_order.internal_id)
        self.assertIsNotNone(self.my_order)


    def test_load_order_from_id(self):
        # test_id = '8a26a525-c6e6-f284-754c-7ebcf221ac7a'
        test_order = self.my_order.load(order_id = self.test_id)
        # print('\nLOAD ORDER FROM ID TEST: ', test_order)
        # print('\nLOAD ORDER FROM ID STATUS TEST: ', test_order.order_status.lower())
        self.assertIn(test_order.order_status.lower(), self.status_options)


    def test_load_order_from_self(self):

        # Load order from exchange based on known order id
        # to avoid having to use funds
        test_order1 = self.my_order.load(order_id = self.test_id)

        # Load order from exchange based on self.order_id
        test_order2 = test_order1.load()

        # print('\nLOAD ORDER TEST: ', test_order2)
        # print('\nLOAD ORDER STATUS TEST: ', test_order2.order_status.lower())
        self.assertIn(test_order2.order_status.lower(), self.status_options)


    def test_cancel_order_via_order_id(self):
        order = self.my_order.load(order_id = self.test_id)
        status = order.cancel()

        # print("\nCANCEL STATUS, ORDER ID: ", status)
        # ERROR: bitmex {"error":{"message":"Not Found","name":"HTTPError"}}
        self.assertIn('bitmex', status)


'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()