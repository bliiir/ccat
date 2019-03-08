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
from ccat.model.database.bucket import Bucket
import ccat.controller.indicator.rsi as rsi
import ccat.controller.helper.df_x_val as df_x_val


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''


class Test_controller_helper_df_x_val(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()

        # Calculate price_close rsi
        cls.price_close_rsi = rsi.get(
            df_in = cls.df_in, id='id',
            data = 'price_close',
            n = 40,
            prefix = 'price_close')

        # print(price_close_rsi)
        cls.rsi_x_val = df_x_val.get(
            df_in = cls.price_close_rsi,
            col = cls.price_close_rsi.columns[1],
            val = 30)


    def test_df_x_val_column_names(self):

        col_names = [
            'id',
            'price_close_rsi',
            'x_value',
            'crossover',
            'crossunder',
            'cross']

        self.assertCountEqual(
            list(self.rsi_x_val.columns.values),
            col_names)


    def test_df_x_val_has_content(self):
        self.assertEqual(len(self.rsi_x_val.tail(10)), 10)


'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()