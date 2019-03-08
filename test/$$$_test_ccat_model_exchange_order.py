# WARNING: This scripts submits two actual orders

'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest
# import inspect

# Third party packages
pass

# Local packages
from ccat.model.exchange.order import Order

'''
------------------------------------------------------------------------
    TESTS
------------------------------------------------------------------------
'''

class Test_model_exchange_order(unittest.TestCase):

	@classmethod
	def setUpClass(cls):

		cls.my_order = Order(market_id=1)

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


	def test_cancel_order_via_self(self):
		order = self.my_order.submit(side = 'sell', amount = 1)
		status = order.cancel()
		self.assertIn('bitmex', status)


	def test_submit(self):
		order = self.my_order.submit(side = 'sell', amount = 1)
		self.test_id = order.order_id
		self.assertIn(order.order_status.lower(), self.status_options)


'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()