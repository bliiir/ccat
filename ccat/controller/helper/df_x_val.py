'''
------------------------------------------------------------------------
    SIGNAL.PY
------------------------------------------------------------------------
SIGNAL calculations. Signals are datapoints that can be directly
inferred from the raw data
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
# import pdb

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

def get(
    df_in,
    col,
    val):
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

    df_out = pd.DataFrame()
    df_out.iloc[0:0]

    # Fill the dataframe with the values from the argument
    df_out['id']=df_in['id']
    df_out[col] = df_in[col].copy()
    df_out['x_value'] = val

    df_out['crossover'] = (
        (df_out[col] > df_out['x_value']) &
        (df_out[col].shift(1) <= df_out['x_value'].shift(1)))

    df_out['crossunder'] = (
        (df_out[col] < df_out['x_value']) &
        (df_out[col].shift(1) >= df_out['x_value'].shift(1)))

    df_out['cross'] = (df_out['crossover']) | df_out['crossunder']

    return df_out