# IMPORTS --------------------------------------------------------------

# Standard library imports
import pdb

# Third party imports
import pandas as pd

# Local application imports
pass


# MODULE ---------------------------------------------------------------

def get(
    df_in:pd.DataFrame,
    id='id',
    data:str='data',
    n:int=14,
    prefix:str='') -> pd.DataFrame:

    '''Calculates the simple moving average (sma) of a given number of
    rows (n) in a given dataframe (df) for a given column (col_data),
    adds the result to an output dataframe(df_out) along with the id and
    returns it.

    Args:

        :df_in (pandas dataframe):
            A Pandas dataframe with an 'id' for merging purposes and a
            'data' column to perform the calculation on.

        :n (int):
            The number of periods/buckets/candles to include in the
            calculation.

        :prefix (str):
            Optional string to be pre-pended to the added field header.


    Returns:

        :df_out (pandas dataframe):
            The amended pandas dataframe with the
            calculated columns appended.
    '''

    # Copy df_in to df_out to avoid aliasing
    df_out = df_in[['id', data]].copy()

    # Assemble the column title
    title = f'{prefix}_sma'
    # print("this worked", title)

    # Calculate ema and store it in column with title assembled above
    df_out[title]=df_out[data].rolling(window=n).mean()

    df_out = df_out[['id', title]]

    return df_out