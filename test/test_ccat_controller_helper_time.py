# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as rd
from math import floor

import pandas as pd

# Local packages
import ccat.controller.helper.time as t
from ccat.model.database.bucket import Bucket


# TESTS ----------------------------------------------------------------


class Test_controller_helper_time(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass


    def test_unix_to_datetime(self):

        market_id = 1
        timeframe_id = 6

        # Get bucket instance
        bucket = Bucket(
            market_id = market_id,
            timeframe_id = timeframe_id)

        # Get bucket dataframe
        df = bucket.read_until(
            time_end = t.now,
            count = 50,
            sort_col = 'time_close',
            sort_dir = 'ASC')

        time1 = t.unix_to_datetime(df, 'time_close')
        time2 = pd.to_datetime(df['time_close'], unit='ms')

        self.assertCountEqual(time1['time_close_ISO'], time2)


    def test_time_duration(self):

        minute = t.minute
        hour = t.hour
        day = t.day
        week = t.week

        self.assertEqual(minute, 60000)
        self.assertEqual(hour, 3600000)
        self.assertEqual(day, 86400000)
        self.assertEqual(week, 604800000)


    def test_time_present(self):

        now = t.now
        # now1 = floor((dt.utcnow().timestamp())*1000)

        # pdb.set_trace()

        self.assertAlmostEqual(
            floor((dt.utcnow().timestamp())),
            floor(now/1000), delta = 100 )


    def test_time_past(self):
        hour_ago = t.hour_ago
        day_ago = t.day_ago
        week_ago = t.week_ago
        month_ago = t.month_ago
        year_ago = t.year_ago

        self.assertAlmostEqual(
            floor(((dt.utcnow() - rd(hours=1)).timestamp())),
            floor(hour_ago/1000),
            delta = 100)

        self.assertAlmostEqual(
            floor(((dt.utcnow() - rd(days=1)).timestamp())),
            floor(day_ago/1000),
            delta = 100)

        self.assertAlmostEqual(
            floor(((dt.utcnow() - rd(weeks=1)).timestamp())),
            floor(week_ago/1000),
            delta = 100)

        self.assertAlmostEqual(
            floor(((dt.utcnow() - rd(months=1)).timestamp())),
            floor(month_ago/1000),
            delta = 100)

        self.assertAlmostEqual(
            floor(((dt.utcnow() - rd(years=1)).timestamp())),
            floor(year_ago/1000),
            delta = 100)


# MAIN -----------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()