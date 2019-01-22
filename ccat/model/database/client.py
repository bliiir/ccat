'''
------------------------------------------------------------------------- - - -
    IMPORTS
------------------------------------------------------------------------- - - -
'''

# Standard library imports
import os

# Third party imports
from sqlalchemy import create_engine

# Local application imports
from ccat import config

'''
------------------------------------------------------------------------- - - -
    CLASSES
------------------------------------------------------------------------- - - -
'''

class Client():

    # Class objects
    dialect     = f'{config.db_dialect}'
    driver      = f'{config.db_driver}'
    user        = f'{config.db_user}'
    password    = f'{config.db_password}'
    host        = f'{config.db_host}'
    name        = f'{config.db_name}'

    params  = f'{dialect}+{driver}://{user}:{password}@{host}/{name}'
    client  = create_engine(params)

    def get():
        return Client.client

'''
------------------------------------------------------------------------
    UNITTEST
------------------------------------------------------------------------
'''
# https://docs.python.org/3.7/library/unittest.html#module-unittest

import unittest
import sqlalchemy

class Test_db_engine(unittest.TestCase):

    def test_db_engine_creation(self):

        db_engine = Db.get()

        self.assertIsInstance(db_engine, sqlalchemy.engine.base.Engine)



'''
------------------------------------------------------------------------- - - -
    MAIN
------------------------------------------------------------------------- - - -
'''

if __name__ == '__main__':

    unittest.main()
