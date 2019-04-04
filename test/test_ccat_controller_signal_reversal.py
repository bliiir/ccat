# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
import pandas as pd

# Local packages
from ccat.model.database.bucket import Bucket
from ccat.controller.signal.reversal import Reversal


# TEST -----------------------------------------------------------------

class Test_controller_signal_reversal_real_data(unittest.TestCase):
    '''Test if the overtraded module returns the expexted results by
    exposing it to a known dataset
    '''


    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 6)

        # Get dataframe with all the market and timeframe data
        cls.df_bucket = cls.b.read_all()

        # Number of candles/buckets to include in the rsi calculation
        len_rsi = 20

        # Get an instance of the Overtraded object
        cls.reversal = Reversal(
            df_bucket = cls.df_bucket,
            len_ma_top = 40,
            len_ma_bottom = 40,
            prefix = 'reversal')


    def test_reversal_get_current_signal(self):
        signal = self.reversal.signal()
        self.assertIn(signal, [0, 1, -1])


    def test_reversal_get_custom_columns(self):

        cols = [
            'id',
            'reversal_signal']

        df = self.reversal.get(cols)

        self.assertCountEqual(cols, df.columns)
        self.assertEqual(10, len(df.head(10)))


    def test_reversal_get_default(self):

        df = self.reversal.get()

        self.assertIsInstance(df, pd.DataFrame)
        # self.assertGreater(len(df.columns), 10)
        self.assertEqual(len(df.tail(10)), 10)


    def test_reversal_short(self):

        df = self.reversal.short()

        self.assertEqual(len(df.columns), 2)
        self.assertEqual(len(df.head(10)), 10)


    def test_reversal_long(self):

        df = self.reversal.long()

        self.assertEqual(len(df.columns), 2)
        self.assertEqual(len(df.head(10)), 10)


    def test_reversal_object_has_get_method(self):
        self.assertIn('long', dir(self.reversal))
        self.assertIn('short', dir(self.reversal))
        self.assertIn('get', dir(self.reversal))



# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()