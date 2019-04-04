'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest
import pdb
from datetime import datetime as dt
# import inspect

# Third party packages
pass

# Local packages
from ccat.controller.helper import time as t
from ccat.model.database.bucket import Bucket


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Test_model_database_bucket(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''
        +------+--------+----------------+
        | id   | name   | milliseconds   |
        |------+--------+----------------|
        | 1    | 1m     | 60000          |
        | 2    | 5m     | 300000         |
        | 3    | 15m    | 900000         |
        | 4    | 1h     | 3600000        |
        | 5    | 4h     | 14400000       |
        | 6    | 1d     | 86400000       |
        | 7    | 7d     | 604800000      |
        | 8    | 30d    | 2592000000     |
        +------+--------+----------------+
        '''

        cls.market_id = 1
        cls.timeframe_id = 6  # TESTS SHOULD BE ON ALL TIMEFRAMES AND MARKETS

        cls.bucket = Bucket(
            market_id=cls.market_id,
            timeframe_id=cls.timeframe_id)

        cls.cols = [
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
            # 'time_close_dt']

        # Set a specific sort column
        cls.sort_col = cls.cols[4]

        # Set a specific sort direction
        cls.sort_dir = 'ASC' # 'DESC'


    def test_model_database_bucket_read_until(self):

        count = 50

        df = self.bucket.read_until(
            time_end = t.now,
            count = count,
            sort_col = self.sort_col,
            sort_dir = self.sort_dir)

        self.assertIsNotNone(df)
        self.assertCountEqual(df.columns, self.cols)
        self.assertEqual(len(df), count)


    def test_model_database_bucket_read_from(self):

        count = 50

        df = self.bucket.read_from(
            time_begin = t.year_ago,
            count = count,
            sort_col = self.sort_col,
            sort_dir = self.sort_dir)

        self.assertIsNotNone(df)
        self.assertCountEqual(df.columns, self.cols)


    def test_model_database_bucket_read_latest(self):

        count = 50

        df = self.bucket.read_latest(
            count=count,
            sort_col = self.sort_col,
            sort_dir = self.sort_dir)

        self.assertIsNotNone(df)
        self.assertCountEqual(df.columns, self.cols)
        self.assertEqual(len(df), count)


    def test_model_database_bucket_read_between(self):

        df = self.bucket.read_between(
            time_begin = t.month_ago,
            time_end = t.now,
            sort_col = self.sort_col,
            sort_dir = self.sort_dir)

        self.assertIsNotNone(df)
        self.assertCountEqual(df.columns, self.cols)
        self.assertEqual(len(df.tail(10)), 10)


    def test_model_database_bucket_read_all(self):

        df = self.bucket.read_all(
            sort_col = self.sort_col,
            sort_dir= self.sort_dir)

        self.assertIsNotNone(df)
        self.assertCountEqual(df.columns, self.cols)
        self.assertEqual(len(df.tail(10)), 10)


    def test_model_database_bucket_custom_update(self):

        count = 500

        df = self.bucket.update(count=count)

        self.assertIsNotNone(df)
        self.assertEqual(len(df), count)


    def test_model_database_bucket_instantiation(self):

        # Check that the primary instance variables are correct
        self.assertEqual(self.bucket.market_id, self.market_id)
        self.assertEqual(self.bucket.timeframe_id, self.timeframe_id)

        # Check that the derived instance are not empty
        self.assertIsNotNone(self.bucket.market_symbol_native)
        self.assertIsNotNone(self.bucket.market_symbol_ccxt)
        self.assertIsNotNone(self.bucket.market_description)
        self.assertIsNotNone(self.bucket.exchange_id)
        self.assertIsNotNone(self.bucket.pair_id)
        self.assertIsNotNone(self.bucket.timeframe_name)
        self.assertIsNotNone(self.bucket.timeframe_ms)
        self.assertIsNotNone(self.bucket.db_client)


    # def test_model_database_bucket_read_execute




'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()