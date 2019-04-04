# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
import pandas as pd
import numpy as np

# Local packages
from ccat import config
from ccat.controller.helper import time as t

from ccat.model.database.bucket import Bucket
from ccat.controller.signal.overtraded import Overtraded
import ccat.controller.helper.df_magic as df_magic


# TESTS ----------------------------------------------------------------

class Test_controller_signal_overtraded_real_data(unittest.TestCase):
    '''Test if the overtraded module returns the expexted results by
    exposing it to a real dataset
    '''

    @classmethod
    def setUpClass(cls):

        cls.len_rsi = 20
        cls.high = 60
        cls.low = 40
        cls.col = 'price_close'
        cls.prefix = 'overtraded'

        # Get a bucket object from Bucket
        cls.bucket = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_bucket = cls.bucket.read_all()

        # Get an instance of the Overtraded object
        cls.overtraded = Overtraded(
            df_bucket = cls.df_bucket,
            len_rsi = cls.len_rsi,
            high = cls.high,
            low = cls.low ,
            col = cls.col,
            prefix = cls.prefix)


    def test_overtraded_get_current_signal_only(self):
        signal = self.overtraded.signal()
        self.assertIn(signal, [0, 1, -1])


    def test_overtraded_get_custom_rows(self):
        df = self.overtraded.get(rows = 1)
        self.assertEqual(len(df), 1)


    def test_overtraded_get_custom_columns(self):

        cols = [
            'id',
            # f'{self.prefix}_long',
            f'{self.prefix}_short',
            f'{self.prefix}_signal']

        df = self.overtraded.get(cols = cols)

        self.assertCountEqual(cols, df.columns)
        self.assertEqual(len(df.columns), len(cols))
        self.assertEqual(len(df.head(10)), 10)


    def test_overtraded_get_default(self):

        df = self.overtraded.get()

        self.assertEqual(len(df.columns), 4)
        self.assertEqual(len(df.head(10)), 10)


    def test_overtraded_short(self):
        df = self.overtraded.short()
        self.assertEqual(len(df.columns), 2)
        self.assertEqual(len(df.head(10)), 10)


    def test_overtraded_long(self):
        df = self.overtraded.long()
        self.assertEqual(len(df.columns), 2)
        self.assertEqual(len(df.head(10)), 10)


    def test_overtraded_pandas_dataframe(self):
        self.df_overtraded = self.overtraded.get()
        self.assertIsInstance(self.df_overtraded, pd.DataFrame)


    def test_overtraded_arguments_passed_ok(self):

        self.assertCountEqual(
            self.df_bucket.columns,
            self.overtraded.df_bucket.columns)

        self.assertEqual(self.len_rsi, self.overtraded.len_rsi)
        self.assertEqual(self.high, self.overtraded.high)
        self.assertEqual(self.low, self.overtraded.low)
        self.assertEqual(self.col, self.overtraded.col_bucket)
        self.assertEqual(self.prefix, self.overtraded.prefix)


    def test_overtraded_not_none(self):
        self.assertIsNotNone(self.overtraded)
        self.assertIsNotNone(self.overtraded.df_bucket)
        self.assertIsNotNone(self.overtraded.len_rsi)
        self.assertIsNotNone(self.overtraded.high)
        self.assertIsNotNone(self.overtraded.low)
        self.assertIsNotNone(self.overtraded.col_bucket)
        self.assertIsNotNone(self.overtraded.prefix)



class Test_controller_signal_overtraded_fake_data(unittest.TestCase):
    '''Test if the overtraded module returns the expexted results by
    exposing it to a known dataset
    '''

    @classmethod
    def setUpClass(cls):

        # Set params
        cls.len_rsi = 20
        cls.high = 60
        cls.low = 40
        cls.col = 'price_close'
        cls.prefix = 'overtraded'

        # Generate fake data
        x = np.arange(0, 10, 0.1)
        y = (np.sin(x) + 1)/2 *1000

        # Create a dataframe with the fake data
        cls.df_in = pd.DataFrame({'price_close':y})

        # Set id column = index and then as the id column for merging
        cls.df_in['id'] = cls.df_in.index
        cls.df_in = cls.df_in[['id', 'price_close']]

        # Get an instance of the Overtraded object
        cls.overtraded = Overtraded(
            df_bucket = cls.df_in,
            len_rsi = cls.len_rsi,
            high = cls.high,
            low = cls.low,
            col = cls.col,
            prefix = cls.prefix)


    def test_overtraded_get_custom_columns(self):

        cols = [
            'id',
            f'{self.prefix}_long',
            # f'{self.prefix}_short',
            f'{self.prefix}_signal']

        df = self.overtraded.get(cols = cols)
        self.assertCountEqual(cols, df.columns)
        self.assertEqual(len(df.columns), len(cols))
        self.assertEqual(len(df.head(10)), 10)


    def test_overtraded_get_default(self):
        df = self.overtraded.get()
        self.assertEqual(len(df.columns), 4)
        self.assertEqual(len(df.head(10)), 10)


    def test_overtraded_short(self):
        df = self.overtraded.short()
        self.assertEqual(len(df.columns), 2)
        self.assertEqual(len(df.head(10)), 10)


    def test_overtraded_long(self):
        df = self.overtraded.long()
        self.assertEqual(len(df.columns), 2)
        self.assertEqual(len(df.head(10)), 10)




# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()