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