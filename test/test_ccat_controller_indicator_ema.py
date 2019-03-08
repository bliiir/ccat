'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest

# Third party packages
import pandas as pd

# Local packages
from ccat.model.database.bucket import Bucket
import ccat.controller.indicator.ema as ema



'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''


class Test_controller_indicator_ema(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()

        # Calculate wick_top ema
        cls.my_ema = ema.get(
            df_in=cls.df_in,
            id='id',
            data='price_close',
            n=12,
            prefix='price_close')


    def test_has_content(self):
        self.assertEqual(len(self.my_ema.tail(10)), 10)


    def test_is_pandas_dataframe(self):
        self.assertIsInstance(self.my_ema, pd.DataFrame)


    def test_ema_not_none(self):
        self.assertIsNotNone(self.my_ema)



'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()