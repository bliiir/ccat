'''
------------------------------------------------------------------------
    INDICATOR.PY
------------------------------------------------------------------------
Indicator calculations. Indicators are datapoints that can be
directly inferred from the raw data and or features
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

# Local application imports
pass


'''
------------------------------------------------------------------------
    FUNCTIONS
------------------------------------------------------------------------
'''


# Exponential Moving Average (EMA)
def get(
    df_in:pd.DataFrame,
    id='id',
    data:str='data',
    n:int=14,
    prefix:str='') -> pd.DataFrame:

    '''Calculates the exponential moving average (EMA) of a given number
    of rows (n) in a given dataframe (df) for the column 'data', adds
    the result to an output dataframe(df_out) along with the 'id' and
    returns it.

    Args:
        :df_in (pandas dataframe):
            The dataframe with the data to base the calculation on.
            It must have the columns 'id' and 'data'

        :n (int):
            The number of periods/buckets/candles to include in the
            calculation

        :prefix (str):
            Optional string to be pre-pended to the field header

    Returns:
        :df_out (pandas dataframe):
            The amended pandas dataframe with the calculated columns
            added
    '''


    # Create a new dataframe to avoid aliasing
    df_out = pd.DataFrame()

    # Copy id column from incoming dataframe to outgoing dataframe
    df_out['id']= df_in['id']

    # Set the df index to the id column
    # df_out.set_index('id', inplace=True)

    # Assemble the column title
    title = f'{prefix}_ema'

    # Calculate ema and store it in a column with title assembled above
    df_out[title]=df_in[data].ewm(span=n, adjust=False).mean()

    return df_out

