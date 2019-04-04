# IMPORTS --------------------------------------------------------------

# Standard library imports
import pdb

# Third party imports
import pandas as pd
import numpy as np
# import pdb

# Local application imports
pass


# MODULE --------------------------------------------------------------

def get(
    df_in:pd.DataFrame,
    col:str,
    val:float,
    prefix:str = ''):
    '''Indicates crossovers of one data columns with a fixed value.
    This is useful for example when testing if the RSI indicator has
    crossed over the 70 oversold threshold

    Takes a pandas dataframes, a float, and the name of the columns to
    perform the operation on as arguments.

    The function creates a new dataframe with only an id column, used
    for merging with other dataframes and maintain correspondance with
    the database.

    A fourth column, crossover, is added where the boolean result of a
    a check if the value of the first data column, named col_1, crosses
    over and/or under the value of the second data column, named col2.

    Args:
        :df_in (pa.DataFrame):
            A pandas dataframe with at least an 'id' column and a data
            column

        :col (str):
            A string with the title of the data column of df_in_1 we
            want to check if crosses over and/or under the data column
            in df_in_2

        :val (str):
            A float with the value to check crossover/unders

    Returns:
        :pd.Dataframe:
            A pandase dataframe with four columns:

                'id':
                    The id that is used to merge and maintain
                    correspondance with the database

                col:
                    A column with df_in[col] data

                'value':
                    A column with the value

                'crossover':
                    Boolen values indicating if the values in col
                    have crossed over 'value'

                'crossunder':
                    Boolen values indicating if the values in col
                    have crossed under 'value'

                'cross':
                    Boolen values indicating if the values in col
                    have crossed 'value'

    '''
    # Create and initialize a new dataframe

    df_out = df_in[['id', col]].copy()

    df_out[f'{prefix}_val'] = val

    df_out[f'{prefix}_crossover'] = (
        (df_out[col] > val) &
        (df_out[col].shift(1) <= val))

    df_out[f'{prefix}_crossunder'] = (
        (df_out[col] < val) &
        (df_out[col].shift(1) >= val))

    df_out[f'{prefix}_cross'] = (
        df_out[f'{prefix}_crossover'] |
        df_out[f'{prefix}_crossunder'])

    df_out = df_out[[
        'id',
        f'{prefix}_val',  # TODO: Do I need this column? The information is available
        f'{prefix}_crossover',
        f'{prefix}_crossunder',
        f'{prefix}_cross']]

    return df_out

