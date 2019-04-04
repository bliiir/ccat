# IMPORTS --------------------------------------------------------------

# Standard library imports
import pdb

# Third party imports
import pandas as pd
# import numpy as np

# Local application imports
pass



# MODULE ---------------------------------------------------------------

def merge(
    dfs:list,
    on:str = 'id') -> pd.DataFrame:
    '''Merge a list of dataframes'''

    # Create dataframe with just the id column from the first
    # dataframe in dfs list
    df_out = dfs[0]['id'].copy()

    # merge the dfs dataframes into the df dataframe
    for i in range(len(dfs)):
        df_out = pd.merge(df_out, dfs[i], on=on)

    return df_out


def crop(
    df_in:pd.DataFrame,
    cols:list = None,
    rows:int = None) -> pd.DataFrame:
    '''Crop a dataframe'''

    # return df_out
    df_out = df_in.copy()


    # Subset dataframe to columns indicated by the cols argument
    if cols != None:

        # Insert id column if there isn't one
        if 'id' not in cols:
            cols.insert(0, 'id')

        # Subset df_out to cols
        df_out =  df_out[cols]

    # Subset the dataframe to the last `rows` rows
    if rows != None:
        df_out = df_out.tail(rows)

    return df_out


def dif(
    df_in:pd.DataFrame,
    col_1:str,
    col_2:str) -> pd.DataFrame:
    '''Calculate the difference between two columns in a pandas
    dataframe
    '''

    df_out = df_in.copy()

    # Calculate the absolute difference
    df_out[f'dif_abs'] = abs(df_out[col_1] - df_out[col_2])

    # Calculate the difference
    df_out[f'{col_1}_-_{col_2}'] = df_out[col_1] - df_out[col_2]

    # Calculate the absolute relative difference
    df_out[f'dif_rel_abs'] = (abs(
        (df_out[col_1] - df_out[col_2]) /
        (df_out[col_1] + df_out[col_2])))

    # Calculate the relative difference
    df_out[f'dif_rel_{col_1}_-_{col_2}'] = (
        (df_out[col_1] - df_out[col_2]) /
        (df_out[col_1] + df_out[col_2]))

    return df_out

