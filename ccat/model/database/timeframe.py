'''
------------------------------------------------------------------------
    TIMEFRAME.PY
------------------------------------------------------------------------
I/O interface layer for the 'timeframe' table in the database.
'''


'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard library imports
pass

# Third party imports
import pandas as pd

# Local application imports
from ccat.model.database.client import Client


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Timeframe():

    def __init__(self, timeframe_id):

        self.timeframe_id = timeframe_id

        # Get the attributes from the timeframe table
        sql = f'SELECT * FROM timeframe \
                WHERE id={self.timeframe_id}'

        df = pd.read_sql(sql=sql, con=Client.get())

        self.name = df.name[0]
        self.ms = df.milliseconds[0]

    def get(self):
        return self

    def get_ms(self):
        return self.ms

    def get_name(self):
        return self.name

'''
------------------------------------------------------------------------
    UNITTEST
------------------------------------------------------------------------
'''
# https://docs.python.org/3.7/library/unittest.html#module-unittest

import unittest

class Test_timeframe(unittest.TestCase):

    def setUp(self):
        pass

    def test_1m_name(self):
        my_timeframe = Timeframe(timeframe_id=1)
        self.assertEqual(my_timeframe.get_name(), '1m')

    def test_1m_ms(self):
        my_timeframe = Timeframe(timeframe_id=1)
        self.assertEqual(my_timeframe.get_ms(), 60000)

    def test_1h_name(self):
        my_timeframe = Timeframe(timeframe_id=4)
        self.assertEqual(my_timeframe.get_name(), '1h')

    def test_1h_ms(self):
        my_timeframe = Timeframe(timeframe_id=4)
        self.assertEqual(my_timeframe.get_ms(), 3600000)

'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()


