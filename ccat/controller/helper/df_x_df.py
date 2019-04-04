# IMPORTS --------------------------------------------------------------

# Standard library imports
import pdb

# Third party imports
import pandas as pd
# import pdb

# Local application imports
pass


# FUNCTIONS ------------------------------------------------------------

def get(
    df_in_1:pd.DataFrame,
    df_in_2:pd.DataFrame,
    col_1:str,
    col_2:str,
    prefix = ''):

    '''Indicates crossovers of two data columns

    Takes two pandas dataframes, and the names of the columns to
    perform the operation on as arguments.

    The function creates a new dataframe with only an id column, used
    for merging with other dataframes and maintain correspondance with
    the database.

    A fourth column, crossover, is added where the boolean result of a
    a check if the value of the first data column, named col_1, crosses
    over and/or under the value of the second data column, named col2.

    Args:
        :df_in_1 (pd.DataFrame):
            A pandas dataframe with at least an 'id' column and a data
            column. This is the signal

        :df_in_2 (pd.DataFrame):
            A pandas dataframe with at least an 'id' column and a data
            column. This is the reference

        :col_1 (str):
            A string with the title of the data column of df_in_1 we
            want to check if crosses over and/or under the data column
            in df_in_2

        :col_2 (str):
            A string with the title of the data column of df_in_2 we
            want to check if is crossed over and/or under by the values
            in the data column in df_in_1

    Returns:
        :pd.Dataframe:
            A pandase dataframe with four columns:

                'id':
                    The id that is used to merge and maintain
                    correspondance with the database

                {col_1}:
                    A column with df_in_1[col_1] data

                {col_2}:
                    A column with df_in_2[col_2] data

                '{}_crossover':
                    Boolen values indicating if the values in col_1
                    have crossed over the values in col_2

                '{}_crossunder':
                    Boolen values indicating if the values in col_1
                    have crossed under the values in col_2

                '{}_cross':
                    Boolen values indicating if the values in col_1
                    have crossed the values in col_2

    '''

    # Merge the two dataframes into one on id
    df_out = pd.merge(
        df_in_1[['id', col_1]],
        df_in_2[['id', col_2]],
        on='id')

    # Calculate crossover
    df_out[f'{prefix}_crossover'] = (
        (df_out[col_1] > df_out[col_2]) &
        (df_out[col_1].shift(1) <= df_out[col_2].shift(1)))

    # Calculate crossunder
    df_out[f'{prefix}_crossunder'] = (
        (df_out[col_1] < df_out[col_2]) &
        (df_out[col_1].shift(1) >= df_out[col_2].shift(1)))

    # Calculate cross
    df_out[f'{prefix}_cross'] = (
        df_out[f'{prefix}_crossover'] | df_out[f'{prefix}_crossunder'])

    # Subset dataframe
    df_out = df_out[[
        'id',
        f'{prefix}_crossover',
        f'{prefix}_crossunder',
        f'{prefix}_cross']]

    return df_out