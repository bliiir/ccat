# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
import pandas as pd
import numpy as np

# Local packages
from ccat.model.database.bucket import Bucket
import ccat.controller.indicator.ema as ema



# TESTS ----------------------------------------------------------------

class Test_controller_indicator_ema_with_real_data(unittest.TestCase):

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


class Test_controller_indicator_ema_with_dummy_data(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.len = 10

        # Generate test data
        cls.y = list(range(0,101))

        # Create a dataframe with the fake data
        cls.df_in = pd.DataFrame()
        cls.df_in['price_close'] = cls.y

       # Set id column = index and then as the id column for merging
        cls.df_in['id'] = cls.df_in.index
        cls.df_in = cls.df_in[['id', 'price_close']]

        # Calculate wick_top ema
        cls.my_ema = ema.get(
            df_in=cls.df_in,
            id='id',
            data='price_close',
            n=cls.len ,
            prefix='price_close')


    def test_dummy_data_adds_up(self):
        df = self.my_ema
        ema_sum = df['price_close_ema'].sum()
        ema_mean = df['price_close_ema'].mean()
        self.assertEqual(ema_sum, 4620.249999960968)
        self.assertEqual(ema_mean, 45.745049504564044)

        # pdb.set_trace()


# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()