# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
import pandas as pd

# Local packages
from ccat import config
from ccat.model.database.bucket import Bucket
from ccat.controller.signal.extreme import Extreme


# TEST -----------------------------------------------------------------

class Test_controller_signal_extreme_real_data(unittest.TestCase):
    '''Test if the extreme module returns the expexted results
    '''

    @classmethod
    def setUpClass(cls):

        cls.len_ma_top = 40
        cls.len_ma_bottom = 40
        cls.prefix = 'extreme'
        cls.l1 = 3.0
        cls.l2 = 1.5
        cls.s1 = 3.0
        cls.s2 = 1.5

        cls.bucket = Bucket(
            market_id = 1,
            timeframe_id = 6)

        # cls.bucket.update()

        cls.df_bucket = cls.bucket.read_all()

        cls.extreme = Extreme(
            df_bucket = cls.df_bucket,
            len_ma_top = cls.len_ma_top,
            len_ma_bottom = cls.len_ma_bottom,
            prefix = cls.prefix,
            l1 = cls.l1,
            l2 = cls.l2,
            s1 = cls.s1,
            s2 = cls.s2)


    def test_extreme_signal_only(self):
        signal = self.extreme.signal()
        self.assertIn(signal, [-1, 0, 1])


    def test_extreme_get_custom_rows(self):

        rows = 5
        df = self.extreme.get(rows = rows)

        self.assertEqual(len(df), rows)


    def test_extreme_get_custom_columns(self):

        cols = [
            'id',
            f'{self.prefix}_signal']

        df = self.extreme.get(cols = cols)

        self.assertCountEqual(df.columns, cols)


    def test_extreme_get_default(self):

        cols = [
            'id',
            f'{self.prefix}_long',
            f'{self.prefix}_short',
            f'{self.prefix}_signal']

        df = self.extreme.get()

        for col in cols:
            self.assertIn(col, list(df.columns.values))

        self.assertEqual(10, len(df.tail(10)))


    def test_extreme_short(self):

        df = self.extreme.short()

        cols = ['id', f'{self.prefix}_short']

        self.assertCountEqual(df.columns, cols)
        self.assertEqual(len(df.tail(10)), 10)


    def test_extreme_long(self):

        df = self.extreme.long()
        cols = ['id', f'{self.prefix}_long']

        self.assertCountEqual(df.columns, cols)
        self.assertEqual(len(df.tail(10)), 10)


    def test_extreme_instance_attributes(self):
        self.assertEqual(self.extreme.prefix, f'{self.prefix}')
        self.assertEqual(len(self.extreme.df_main.tail(10)), 10)


    def test_extreme_object_has__methods(self):
        self.assertIn('get', dir(self.extreme))
        self.assertIn('long', dir(self.extreme))
        self.assertIn('short', dir(self.extreme))



# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()