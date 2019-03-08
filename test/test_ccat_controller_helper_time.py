'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest
import pdb
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta as rd
from math import floor

# Third party packages
pass

# Local packages
import ccat.controller.helper.time as t


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''


class Test_controller_helper_time(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):

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

        self.assertEqual(
            floor((dt.now().timestamp())),
            floor(now/1000) )


    def test_time_past(self):
        hour_ago = t.hour_ago
        day_ago = t.day_ago
        week_ago = t.week_ago
        month_ago = t.month_ago
        year_ago = t.year_ago

        self.assertAlmostEqual(
            floor(((dt.now() - rd(hours=1)).timestamp())),
            floor(hour_ago/1000),
            places = 7)

        self.assertAlmostEqual(
            floor(((dt.now() - rd(days=1)).timestamp())),
            floor(day_ago/1000),
            places = 7)

        self.assertAlmostEqual(
            floor(((dt.now() - rd(weeks=1)).timestamp())),
            floor(week_ago/1000),
            places = 7)

        self.assertAlmostEqual(
            floor(((dt.now() - rd(months=1)).timestamp())),
            floor(month_ago/1000),
            places = 7)

        self.assertAlmostEqual(
            floor(((dt.now() - rd(years=1)).timestamp())),
            floor(year_ago/1000),
            places = 7)

'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()