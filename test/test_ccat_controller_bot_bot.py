# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb
import sys
# from datetime import datetime as dt
# import argparse
# from unittest.mock import patch
# import inspect

# Third party packages
pass


# Local packages
import ccat.controller.bot.bot as bot


# CLASSES --------------------------------------------------------------

class Test_controller_bot_bot(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        bot.market_id = 1
        bot.timeframe_id = 6
        bot.count = 500


    def setUp(self):
        pass


    def test_controller_bot_short(self):

        bot.signal = -1
        bot.stake_size = 1
        trade = bot.execute(bot.signal)

        self.assertIsNotNone(bot)
        self.assertEqual(trade.order['info']['side'], 'Sell')
        self.assertEqual(trade.order_status, 'Filled')


    def test_controller_bot_long(self):

        bot.signal = 1
        bot.stake_size = 1
        trade = bot.execute(bot.signal)

        self.assertIsNotNone(bot)
        self.assertEqual(trade.order['info']['side'], 'Buy')
        self.assertEqual(trade.order_status, 'Filled')


    def test_controller_bot_no_trade(self):

        bot.signal = 0
        trade = bot.execute(bot.signal)

        self.assertIsNotNone(bot)
        self.assertEqual(trade.order_status, '-')



# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()