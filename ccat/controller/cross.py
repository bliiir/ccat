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

def df_x_df(df_in_1, df_in_2, col_1:str, col_2:str):

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



def df_x_val(
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
    df_out[col] = df_in[col]
    df_out['x_value'] = val

    # Pass the dataframe twice to the df_x_df() function
    return df_x_df(df_out, df_out, col, 'x_value')


'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    # Imports
    from ccat import bucket
    from ccat import feature
    from ccat import indicator

    b = bucket.Bucket(market_id=1,timeframe_id=1)

    # Update the table
    b.update()

    # Get a dataframe with all the data for the market and timeframe
    df_in = b.read_all()

    # Calculate the wicks
    df_height = feature.height(df_in)

    # Calculate wick_top sma
    wick_top_sma = indicator.ema(
        df_in=df_height, id='id',
        data='height_top',
        n=40,
        prefix='height_top')

    # print(wick_top_sma)
    # print(wick_top_sma.columns[1])

    # Calculate wick_bottom sma
    wick_bottom_sma = indicator.ema(
        df_in=df_height, id='id',
        data='height_bottom',
        n=40,
        prefix='height_bottom')

    # print(wick_bottom_sma)
    # print(wick_bottom_sma.columns[1])

    crossover_wick_ema = df_x_df(
        df_in_1 = wick_top_sma,
        df_in_2 = wick_bottom_sma,
        col_1 = wick_top_sma.columns[1],
        col_2 = wick_bottom_sma.columns[1])


    print(crossover_wick_ema)

