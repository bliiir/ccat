'''
------------------------------------------------------------------------- - - -
    IMPORTS
------------------------------------------------------------------------- - - -
'''

# Standard library imports
import os

# Third party packages
pass

# Local packages
pass

'''
------------------------------------------------------------------------- - - -
    ENVIRONMENT
------------------------------------------------------------------------- - - -
'''

# Database
db_dialect = os.environ["DB_DIALECT"]
db_driver = os.environ["DB_DRIVER"]
db_host = os.environ["DB_HOST"]
db_name = os.environ["DB_NAME"]
db_user = os.environ["DB_UN"]
db_password = os.environ['DB_PW']

# log files
lf_bot = os.environ["LF_BOT"]
lf_bucket_update = os.environ["LF_BUCKET_UPDATE"]
lf_bucket_historical = os.environ["LF_BUCKET_HISTORICAL"]
