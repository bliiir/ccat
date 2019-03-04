'''
------------------------------------------------------------------------
    DF_CROP.PY
------------------------------------------------------------------------
Crops a dataframe to contain a specific list of columns
- always including the id column


##### NOT READY AND NOT USED #####


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

# def merge(
#     df_1:pd.DataFrame,
#     df_2:pd.DataFrame,
#     on:str = 'id') -> pd.DataFrame:
#     '''Merge two dataframes
#     I don't really need this - the pd.merge() command does the same thing'''

#     df_out = pd.DataFrame()
#     df_out = pd.merge(df_1, df_2, on=on)

#     return df_out



def crop(
    df_in:pd.DataFrame,
    cols:list) -> pd.DataFrame:
    '''Crop a dataframe'''

    # Ensure id is included in the list of columns
    if 'id' not in cols:
        cols.insert(0, 'id')

    # Crop the dataframe
    df_out = pd.DataFrame()
    df_out = df_in[cols].copy()

    return df_out



def diff(
    df_in:pd.DataFrame,
    col_1:str,
    col_2:str) -> pd.DataFrame:
    '''Calculate the difference between two columns in a pandas
    dataframe
    '''

    df_out = df_in.copy()

    # Calculate the difference
    df_out['diff_actual'] = df_out[col_1] - df_out[col_2]
    df_out['diff_relative'] = (
        (df_out[col_1] - df_out[col_2]) /
        (df_out[col_1] + df_out[col_2]))

    return df_out

