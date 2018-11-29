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

class Sql_engine():

    # Class objects
    params = f'{cf.pg_dialect}+{cf.pg_driver}://{cf.pg_user}:{cf.pg_password}@{cf.pg_host}/{cf.pg_name}'
    engine = create_engine(params)

    def get():
        return Sql_engine.engine


'''
------------------------------------------------------------------------- - - -
    SCOPE CHECK
------------------------------------------------------------------------- - - -
'''

# Run if executed directly. Do not run it if import
if __name__ == '__main__':
    ngn = Sql_engine.get()
    print(ngn)
