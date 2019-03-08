'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest

# Third party packages
import sqlalchemy

# Local packages
from ccat.model.database.client import Client



'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''


class Test_model_database_client(unittest.TestCase):

    def test_model_database_client_creation(self):

        db_engine = Client.get()

        self.assertIsInstance(db_engine, sqlalchemy.engine.base.Engine)


'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()