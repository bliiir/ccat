# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
import pandas as pd

# Local packages
from ccat.model.database.bucket import Bucket
import ccat.controller.indicator.rsi as rsi



# TESTS ----------------------------------------------------------------

class Test_controller_indicator_rsi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id=1,
            timeframe_id=1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()

        # Calculate price_close rsi
        cls.my_rsi = rsi.get(
            df_in=cls.df_in,
            id='id',
            data='price_close',
            n=12,
            prefix='price_close')


    def test_has_content(self):
        self.assertEqual(len(self.my_rsi.tail(10)), 10)


    def test_is_pandas_dataframe(self):
        self.assertIsInstance(self.my_rsi, pd.DataFrame)


    def test_rsi_not_none(self):
        self.assertIsNotNone(self.my_rsi)



# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()