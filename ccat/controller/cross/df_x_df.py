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

def get(df_in_1, df_in_2, col_1:str, col_2:str):

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

                col_1:
                    A column with df_in_1[col_1] data

                col_2:
                    A column with df_in_2[col_2] data

                'crossover':
                    Boolen values indicating if the values in col_1
                    have crossed over the values in col_2

                'crossunder':
                    Boolen values indicating if the values in col_1
                    have crossed under the values in col_2

                'cross':
                    Boolen values indicating if the values in col_1
                    have crossed the values in col_2

    '''

    # Merge the two dataframes into one on key id

    df_in = pd.merge(df_in_1[['id', col_1]], df_in_2[['id', col_2]])

    # breakpoint()
    df_out = pd.DataFrame()
    df_out.iloc[0:0]

    df_out['id']=df_in['id']
    df_out[col_1] = df_in[col_1].copy()
    df_out[col_2] = df_in[col_2].copy()

    df_out['crossover'] = ((df_in[col_1] > df_in[col_2]) &
        (df_in[col_1].shift(1) <= df_in[col_2].shift(1)))

    df_out['crossunder'] = ((df_in[col_1] < df_in[col_2]) &
        (df_in[col_1].shift(1) >= df_in[col_2].shift(1)))

    df_out['cross'] = (df_out['crossover']) | df_out['crossunder']

    return df_out


'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    # Imports
    from ccat import bucket
    from ccat import height
    from ccat import ema

    b = bucket.Bucket(market_id=1,timeframe_id=1)

    # Update the table
    b.update()

    # Get a dataframe with all the data for the market and timeframe
    df_in = b.read_all()

    # Calculate the wicks
    df_height = height.get(df_in)

    # Calculate wick_top ema
    wick_top_sma = ema.get(
        df_in=df_height, id='id',
        data='height_top',
        n=40,
        prefix='height_top')

    # Calculate wick_bottom ema
    wick_bottom_sma = ema.get(
        df_in=df_height, id='id',
        data='height_bottom',
        n=40,
        prefix='height_bottom')

    crossover_wick_ema = get(
        df_in_1 = wick_top_sma,
        df_in_2 = wick_bottom_sma,
        col_1 = wick_top_sma.columns[1],
        col_2 = wick_bottom_sma.columns[1])

    print(crossover_wick_ema)

