'''
------------------------------------------------------------------------- - - -
    IMPORTS
------------------------------------------------------------------------- - - -
'''

# Standard library imports
import os
import time
import datetime
from math import floor

'''
------------------------------------------------------------------------- - - -
    CONFIG
------------------------------------------------------------------------- - - -
'''

# Database
db_dialect = os.environ["DB_DIALECT"]
db_driver = os.environ["DB_DRIVER"]
db_host = os.environ["DB_HOST"]
db_name = os.environ["DB_NAME"]
db_user = os.environ["DB_UN"]
db_password = os.environ["DB_PW"]

# log files
lf_bucket_update = os.environ["LF_BUCKET_UPDATE"]
lf_bucket_historical = os.environ["LF_BUCKET_HISTORICAL"]



# Time
def now():
    return floor((datetime.datetime.now().timestamp())*1000)

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
    print('datetime.datetime: \t', now())
    print('time.time: \t\t', time.time())
    print('your tz: \t\t', datetime.datetime.fromtimestamp(now()/1000))
    print('utc: \t\t\t', datetime.datetime.utcfromtimestamp(now()/1000))

























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
