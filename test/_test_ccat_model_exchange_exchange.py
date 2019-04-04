# WARNING: This scripts submits one actual order

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
from ccat.model.database.market import Market
from ccat.model.exchange.exchange import Exchange

'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

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

		self.assertIn('timestamp', self.new_order)
		self.assertIn('orderID', self.new_order['info'])


'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()