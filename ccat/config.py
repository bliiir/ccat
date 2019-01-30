'''
------------------------------------------------------------------------- - - -
    IMPORTS
------------------------------------------------------------------------- - - -
'''

# Standard library imports
import os
import time
import datetime
from math import floor

'''
------------------------------------------------------------------------- - - -
    CONFIG
------------------------------------------------------------------------- - - -
'''

# Database
db_dialect = os.environ["DB_DIALECT"]
db_driver = os.environ["DB_DRIVER"]
db_host = os.environ["DB_HOST"]
db_name = os.environ["DB_NAME"]
db_user = os.environ["DB_UN"]
db_password = os.environ['DB_PW']

# log files
lf_bucket_update = os.environ["LF_BUCKET_UPDATE"]
lf_bucket_historical = os.environ["LF_BUCKET_HISTORICAL"]


# Time
def now():
    return floor((datetime.datetime.now().timestamp())*1000)

def hour_ago():
    return now()-3600000

def day_ago():
    return now()-86400000

def week_ago():
    return now()-604800000

def month_ago():
    return now()-2592000000


'''
------------------------------------------------------------------------
    UNITTEST
------------------------------------------------------------------------
'''

import unittest

class Test_market(unittest.TestCase):

    def setUp(self):
        pass

    def test_environment_variables(self):
        pass

    def test_now(self):
        self.assertIsInstance(now(), int)

    def test_hour_ago(self):
        self.assertIsInstance(hour_ago(), int)

    def test_day_ago(self):
        self.assertIsInstance(day_ago(), int)

    def test_week_ago(self):
        self.assertIsInstance(week_ago(), int)

    def test_month_ago(self):
        self.assertIsInstance(month_ago(), int)



'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()

'''
------------------------------------------------------------------------- - - -
    MAIN
------------------------------------------------------------------------- - - -
'''

# Run if executed directly. Do not run it if import
if __name__ == '__main__':
    print('datetime.datetime: \t', now())
    print('time.time: \t\t', time.time())
    print('your tz: \t\t', datetime.datetime.fromtimestamp(now()/1000))
    print('utc: \t\t\t', datetime.datetime.utcfromtimestamp(now()/1000))
