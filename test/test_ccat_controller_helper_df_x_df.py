# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest

# Third party packages
import pandas as pd

# Local packages
from ccat.model.database.bucket import Bucket
import ccat.controller.feature.height as height
import ccat.controller.indicator.sma as sma
import ccat.controller.helper.df_x_df as df_x_df


# TESTS ----------------------------------------------------------------

class Test_controller_helper_df_x_df(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.prefix = 'test'

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()

        # Calculate the wicks
        cls.df_height = height.get(cls.df_in)

        # Calculate wick_top ema
        cls.wick_top_sma = sma.get(
            df_in = cls.df_height,
            id = 'id',
            data = 'abs_top',
            n = 40,
            prefix = 'abs_top')

        # Calculate wick_bottom ema
        cls.wick_bottom_sma = sma.get(
            df_in = cls.df_height, id='id',
            data = 'abs_bottom',
            n = 40,
            prefix = 'abs_bottom')

        cls.crossover_wick_ema = df_x_df.get(
            df_in_1 = cls.wick_top_sma,
            df_in_2 = cls.wick_bottom_sma,
            col_1 = cls.wick_top_sma.columns[1],
            col_2 = cls.wick_bottom_sma.columns[1],
            prefix = cls.prefix)


    def test_df_x_df_column_names(self):

        col_names = [
            'id',
            f'{self.prefix}_crossover',
            f'{self.prefix}_crossunder']
            # f'{self.prefix}_cross']

        for col_name in col_names:
            self.assertIn(col_name, list(self.crossover_wick_ema.columns.values))


    def test_df_x_df_not_empty(self):
        self.assertGreater(len(self.crossover_wick_ema), 1)

    def test_df_x_df_pd_dataframe(self):
        self.assertIsInstance(self.crossover_wick_ema, pd.DataFrame)

    def test_df_x_df_not_none(self):
        self.assertIsNotNone(self.crossover_wick_ema)


# MAIN --------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()