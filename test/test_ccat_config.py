'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest
import pdb
import os
from datetime import datetime as dt
# import inspect

# Third party packages
pass

# Local packages
from ccat import config
from ccat.model.database.bucket import Bucket


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''

class Test_market(unittest.TestCase):

    def setUp(self):
        self.db_dialect = config.db_dialect
        self.db_driver = config.db_driver
        self.db_host = config.db_host
        self.db_name = config.db_name
        self.db_user = config.db_user
        self.db_password = config.db_password


    def test_environment_variables(self):
        self.assertEqual(self.db_dialect, os.environ["DB_DIALECT"])
        self.assertEqual(self.db_driver, os.environ["DB_DRIVER"])
        self.assertEqual(self.db_host, os.environ["DB_HOST"])
        self.assertEqual(self.db_name, os.environ["DB_NAME"])
        self.assertEqual(self.db_user, os.environ["DB_UN"])
        self.assertEqual(self.db_password, os.environ["DB_PW"])


    def test_environment_variables_strings(self):
        self.assertIsInstance(self.db_dialect, str)
        self.assertIsInstance(self.db_driver, str)
        self.assertIsInstance(self.db_host, str)
        self.assertIsInstance(self.db_name, str)
        self.assertIsInstance(self.db_user, str)
        self.assertIsInstance(self.db_password, str)


    def test_environment_variables_length(self):
        self.assertGreater(len(self.db_dialect), 3)
        self.assertGreater(len(self.db_driver), 3)
        self.assertGreater(len(self.db_host), 3)
        self.assertGreater(len(self.db_name), 3)
        self.assertGreater(len(self.db_user), 3)
        self.assertGreater(len(self.db_password), 3)


'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()