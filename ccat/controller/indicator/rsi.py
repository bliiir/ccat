# IMPORTS --------------------------------------------------------------

# Standard library imports
import pdb

# Third party imports
import pandas as pd

# Local application imports
pass


# MODULE ---------------------------------------------------------------

# Relative Strength Index (RSI)
def get(
    df_in:pd.DataFrame,
    id:str = 'id',
    data:str = 'data',
    n:int = 14,
    prefix:str = '') -> pd.DataFrame:

    '''Calculates the relative strength index (RSI) of a given number of
    rows (n) in a given dataframe (df) for the column 'data', adds the
    result to an output dataframe(df_out) along with the 'id' and
    returns it.

    https://www.iexplain.org/rsi-how-to-calculate-it/

    Args:
        :df_in (pandas dataframe):
            The dataframe with the data to base the calculation on.

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
    df = pd.DataFrame()

    # Copy id column from incoming dataframe to outgoing dataframe
    # df['id']= df_in['id']
    df = df_in[['id', data]].copy()

    # Set the df index to the id column
    # df.set_index('id', inplace=True)

    # Assemble the column title
    title = f'{prefix}_rsi'

    # Calculate difference between current and previous row. Drop NaN's
    delta = df_in[data].diff() #.dropna()

    # Create a copy of the delta df
    gain = delta.copy()

    # Remove negative values
    gain[gain < 0] = 0

    #Average Gain = Total gains / n
    avg_gain = gain.ewm(span=n, adjust=False).mean()

    # Create a copy of the delta df
    loss = delta.copy()

    # Remove positive values
    loss[loss > 0] = 0
    loss = loss.abs()

    # Average Loss = Total loss / n
    avg_loss = loss.ewm(span=n, adjust=False).mean()

    # Calculate the relative strenght
    rs = avg_gain / avg_loss

    # Calculate the relative strength index
    rsi = 100 - 100/(1+rs)
    # rsi = rsi.fillna(50)

    df[title] = rsi

    return df[['id',title]]
