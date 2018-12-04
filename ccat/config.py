'''
------------------------------------------------------------------------- - - -
    IMPORTS
------------------------------------------------------------------------- - - -
'''

# Standard library imports
import os
import time
from math import floor

'''
------------------------------------------------------------------------- - - -
    CONFIG
------------------------------------------------------------------------- - - -
'''

# Database
db_dialect = "postgresql"
db_driver = "psycopg2"
db_host = "localhost"
db_name = "bit_002"
db_user = os.environ["POSTGRES_UN"]
db_password = os.environ['POSTGRES_PW']

# Time
def now():
    return floor(time.time()*1000)

def hour_ago():
    return now()-3600000

def day_ago():
    return now()-86400000

def week_ago():
    return now()-604800000

def month_ago():
    return now()-2592000000

'''
------------------------------------------------------------------------- - - -
    MAIN
------------------------------------------------------------------------- - - -
'''

# Run if executed directly. Do not run it if import
if __name__ == '__main__':
    print(month_ago)

























# ----------------------------------------------------------------------
# PARSER (maybe later)
# ----------------------------------------------------------------------

# Tutorial can be found here: http://www.postgresqltutorial.com/postgresql-python/connect/

# #!/usr/bin/python
# from configparser import ConfigParser


# def config(filename='database.ini', section='postgresql'):
#     # create a parser
#     parser = ConfigParser()
#     # read config file
#     parser.read(filename)

#     # get section, default to postgresql
#     db = {}
#     if parser.has_section(section):
#         params = parser.items(section)
#         for param in params:
#             db[param[0]] = param[1]
#     else:
#         raise Exception('Section {0} not found in the {1} file'.format(section, filename))

#     return db


# if __name__ == '__main__':
#     print(config())
