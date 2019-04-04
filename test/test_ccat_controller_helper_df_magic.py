# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
import pandas as pd
import numpy as np

# Local packages
from ccat.model.database.bucket import Bucket
import ccat.controller.helper.df_magic as df_magic


# TESTS --------------------------------------------------------------


class Test_controller_helper_df_magic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(market_id = 1, timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()


    def test_df_bucket_column_names(self):

        assumed_cols = [
            'id',
            'market_id',
            'timeframe_id',
            'time_open',
            'time_close',
            'time_updated',
            'price_open',
            'price_high',
            'price_close',
            'price_low',
            'volume']

        actual_cols = list(self.df_in.columns.values)

        self.assertCountEqual(actual_cols, assumed_cols)


    def test_df_magic_diff(self):

        cols = ['id', 'A', 'B']

        df_in = pd.DataFrame({
            cols[0]: range(0,100),
            cols[1]: np.random.randint(0,100, 100),
            cols[2]: np.random.randint(0,100, 100)})

        df_out = df_magic.dif(
            df_in = df_in,
            col_1 = cols[1],
            col_2 = cols[2])


    def test_df_magic_crop(self):
        col_names = ['price_high', 'price_low']
        df_out = df_magic.crop(self.df_in, col_names)
        self.assertCountEqual(list(df_out.columns.values), col_names)

    def test_df_magic_merge(self):

        # Create two dataframes with columns id for both and A for one
        # of the dataframes and B for the other
        df1 = pd.DataFrame({
            'id': range(0,100),
            'A': np.random.randint(0,100, 100)})

        df2 = pd.DataFrame({
            'id': range(0,100),
            'B': np.random.randint(0,100, 100)})

        # Merge the two dataframes
        df = df_magic.merge(dfs = [df1, df2], on = 'id')

        # Assert that the content of the A and B columns are the same
        # in the original dataframe and the merged dataframe
        self.assertCountEqual(df1['A'], df['A'])
        self.assertCountEqual(df2['B'], df['B'])




# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()