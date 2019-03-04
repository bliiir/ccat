'''
------------------------------------------------------------------------
    TESTS_THAT_COST_MONEY.PY
------------------------------------------------------------------------
This script submits 3 orders of $1 to bitmex.

'''


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
from ccat.model.database.market import Market

from ccat.model.exchange.exchange import Exchange
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


	# CAREFUL - this submits a real market order to the exchange
	def test_cancel_order_via_self(self):
		order = self.my_order.submit(side = 'sell', amount = 1)
		status = order.cancel()
		self.assertIn('bitmex', status)

		# print("\nCANCEL STATUS, SELF: ", status)
		# ERROR: bitmex cancelOrder() failed: Unable to cancel order due to existing state: Filled


	# CAREFUL - this submits a real market order to the exchange
	def test_submit(self):
		order = self.my_order.submit(side = 'sell', amount = 1)
		# print('\nSTATUS: ', order.order_status)
		# print('\nORDER ID: ', order.order_id)
		self.test_id = order.order_id
		self.assertIn(order.order_status.lower(), self.status_options)


class Test_model_exchange_exchange(unittest.TestCase):

	@classmethod
	def setUpClass(cls):

		cls.market_id = 1
		cls.market = Market(market_id = cls.market_id)

		# Get exchange_id from market_id
		cls.exchange_id = cls.market.get_exchange_id()

		# Create an exchange instance
		cls.exchange = Exchange(exchange_id = cls.exchange_id)

		# Get an exchange client
		cls.exchange_client = cls.exchange.client()


	def test_create_order(self):
		self.new_order = self.exchange_client.create_order(
			side='sell',
			symbol='BTC/USD',
			type='market',
			amount=1,
			)
		# print('New order: ', self.new_order)
		self.assertIn('timestamp', self.new_order)
		self.assertIn('orderID', self.new_order['info'])


'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()