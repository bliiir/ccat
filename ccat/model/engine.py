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
import ccat.config as cf


'''
------------------------------------------------------------------------- - - -
    CLASSES
------------------------------------------------------------------------- - - -
'''

class SqlEngine():

    # Class objects
    params = f'{cf.pg_dialect}+{cf.pg_driver}://{cf.pg_user}:{cf.pg_password}@{cf.pg_host}/{cf.pg_name}'
    engine = create_engine(params)

    def get():
        return SqlEngine.engine


'''
------------------------------------------------------------------------- - - -
    SCOPE CHECK
------------------------------------------------------------------------- - - -
'''

# Run if executed directly. Do not run it if import
if __name__ == '__main__':
    ngn = SqlEngine.get()
    print(ngn)
