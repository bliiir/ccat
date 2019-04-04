# IMPORTS --------------------------------------------------------------

# Standard packages
import unittest
import pdb

# Third party packages
pass

# Local packages
from ccat.model.database.timeframe import Timeframe


# TESTS --------------------------------------------------------------

class Test_model_database_timeframe(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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


# MAIN --------------------------------------------------------------

if __name__ == '__main__':

    unittest.main()