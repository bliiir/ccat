'''
------------------------------------------------------------------------
    DIFF.PY
------------------------------------------------------------------------
Calculates the actual and relative difference between two data-series
'''


'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard library imports
pass

# Third party imports
import pandas as pd
# import numpy as np

# Local application imports
pass

'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''
pass


'''
------------------------------------------------------------------------
    FUNCTIONS
------------------------------------------------------------------------
'''


def get(df_in_1:pd.DataFrame, df_in_2:pd.DataFrame, col_1:str, col_2:str) -> pd.DataFrame:
    '''Calculate the difference between to data-series
    '''
    df_out = pd.DataFrame()

    # Copy id column from incoming dataframe to outgoing dataframe
    df_out['id']= df_in['id'].copy()

    # Set the df index to the id column
    df_out.set_index('id')

    # Copy the incoming data-series to the outgoing dataframe
    df_out[col_1] = df_in_1[col_1].copy()
    df_out[col_2] = df_in_2[col_2].copy()

    # Calculate the difference
    df_out['diff_actual'] = df_in[col_1] - df_in[col_2]
    df_out['diff_relative'] = (
        (df_in[col_1] - df_in[col_2]) /
        (df_in[col_1] + df_in[col_2]))

    return df_out


'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    from ccat import bucket

    # Get a bucket object from Bucket
    b = bucket.Bucket(market_id=1,timeframe_id=1)

    # Update the table
    b.update()

    # Get a dataframe with all the data for the market and timeframe
    df_in = b.read_all()

    # Calculate the diffs
    d = get(df_in, df_in, 'price_high', 'price_low')
    print(d)



