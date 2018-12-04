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
from ccat import config as cf

'''
------------------------------------------------------------------------- - - -
    CLASSES
------------------------------------------------------------------------- - - -
'''

class Db():

    # Class objects
    params = f'{cf.db_dialect}+{cf.db_driver}://{cf.db_user}:{cf.db_password}@{cf.db_host}/{cf.db_name}'
    engine = create_engine(params)

    def get():
        return Db.engine


'''
------------------------------------------------------------------------- - - -
    SCOPE CHECK
------------------------------------------------------------------------- - - -
'''

# Run if executed directly. Do not run it if import
if __name__ == '__main__':
    ngn = Db.get()
    print(ngn)
