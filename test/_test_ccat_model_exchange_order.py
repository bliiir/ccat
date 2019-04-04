# WARNING: This scripts submits two actual orders

# IMPORTS ---------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
pass

# Local packages
from ccat.model.exchange.order import Order


# TESTS ---------------------------------------------------------------

class Test_model_exchange_order(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.order = Order(market_id=1)

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

        cls.my_order = cls.order.submit(side = 'sell', amount = 1)
        cls.test_id = cls.my_order.order_id


    def test_6_cancel_order_via_order_id(self):
        order = self.order.load(order_id = self.test_id)
        status = order.cancel()
        self.assertIn('ERROR', status)


    def test_5_cancel_order_via_self(self):
        status = self.my_order.cancel()
        self.assertIn('ERROR', status)


    def test_4_load_order_from_self(self):
        from_id = self.order.load(order_id = self.test_id)
        from_self = from_id.load()
        self.assertIn(from_self.order_status.lower(), self.status_options)


    def test_3_load_order_from_id(self):
        from_id = self.order.load(order_id = self.test_id)
        self.assertIn(from_id.order_status.lower(), self.status_options)


    def test_2_status(self):
        self.assertIn(self.order.order_status.lower(), self.status_options)


    def test_1_str_(self):
        self.assertIn("order_status", self.order.__str__())


    def test_0_order_not_none(self):
        self.assertIsNotNone(self.order)



# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()