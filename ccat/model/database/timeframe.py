# IMPORTS --------------------------------------------------------------

# Standard library imports
pass

# Third party imports
import pandas as pd

# Local application imports
from ccat.model.database.client import Client


# MODULE --------------------------------------------------------------

class Timeframe():
    '''I/O interface layer for the 'timeframe' table in the database.
    '''

    def __init__(self, timeframe_id):

        self.timeframe_id = timeframe_id

        # Get the attributes from the timeframe table
        sql = f'SELECT * FROM timeframe \
                WHERE id={self.timeframe_id}'

        df = pd.read_sql(sql=sql, con=Client.get())

        self.name = df.name[0]
        self.ms = df.milliseconds[0]

    def get(self):
        return self

    def get_ms(self):
        return self.ms

    def get_name(self):
        return self.name
