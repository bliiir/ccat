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
    df_out = pd.DataFrame()

    # Copy id column from incoming dataframe to outgoing dataframe
    df_out['id']= df_in['id']

    # Set the df index to the id column
    df_out.set_index('id')

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

    df_out[title] = rsi

    return df_out


'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

# See if it works
if __name__ == '__main__':

    # imports
    from ccat import bucket
    from ccat import height

    # Get a bucket object from Bucket
    b = bucket.Bucket(market_id=1,timeframe_id=1)

    # Update the table
    b.update()

    # Get a dataframe with all the data for the market and timeframe
    df_in = b.read_all()

    # Calculate the wicks
    df_height = height.get(df_in)

    # Calculate price_close rsi
    my_rsi = get(
        df_in=df_in, id='id',
        data='price_close',
        n=12,
        prefix='price_close')

    print(my_rsi)
