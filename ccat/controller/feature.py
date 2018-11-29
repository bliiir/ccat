'''
------------------------------------------------------------------------
    FEATURE.PY
------------------------------------------------------------------------
Feature calculations. Features are datapoints that can be directly
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
import numpy as np

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

def height(df_in: pd.DataFrame) -> pd.DataFrame:

    '''Calculates the height of the candle and its elements - total,
    body top-wick and bottom-wick

    Args:
        :df_in (pandas dataframe):  Dataframe with (at least) columns:
            price_open,
            price_high,
            price_low,
            price_close,
            volume

    Returns:
        :df_out (pandas dataframe): Dataframe with (exactly) columns:

            height_total:
                Difference between the price_high and
                price_low denominated in the quota asset,

            height_body:
                Difference between the price_close and
                price_open denominated in the quota asset,

            height_top:
                Difference between the price_close (if higher than
                price_open, and price_open if not) and price_high
                denominated in the quota asset,

            height_bottom:
                Difference between the price_close (if lower than
                price_open, and price_open if not) and price_high
                denominated in the quota asset,

            percent_top:
                height_total/height_top,

            percent_bottom:
                height_total/height_bottom
    '''

    df_out = pd.DataFrame()

    # Copy id column from incoming dataframe to outgoing dataframe
    df_out['id']= df_in['id']

    # Set the df index to the id column
    df_out.set_index('id')

    # Total height
    df_out['height_total']=df_in.price_high-df_in.price_low

    # Body height
    df_out['height_body']=df_in.price_close-df_in.price_open

    # Top wick height
    df_out['height_top']=np.where(
                                df_in.price_close >= df_in.price_open,
                                df_in.price_high - df_in.price_close,
                                df_in.price_high - df_in.price_open)

    # Bottom wick height
    df_out['height_bottom']=np.where(
                                df_in.price_close < df_in.price_open,
                                df_in.price_close - df_in.price_low ,
                                df_in.price_open - df_in.price_low)

    # Top Wick height percentage of total candle height
    df_out['percent_top']=(
                                df_out['height_top'] /
                                df_out['height_total'])

    # Bottom Wick height percentage of total candle height
    df_out['percent_bottom'] = (
                                df_out['height_bottom'] /
                                df_out['height_total'])

    return df_out


def diff(df_in:pd.DataFrame, col_1:str, col_2:str) -> pd.DataFrame:
    '''Calculate the difference between to data-series
    '''
    df_out = pd.DataFrame()

    # Copy id column from incoming dataframe to outgoing dataframe
    df_out['id']= df_in['id']

    # Set the df index to the id column
    df_out.set_index('id')

    # Copy the incoming data-series to the outgoing dataframe
    df_out[col_1] = df_in[col_1]
    df_out[col_2] = df_in[col_2]

    # Calculate the difference
    df_out['diff'] = df_in[col_1] - df_in[col_2]

    return df_out



def diff_percent(df_in:pd.DataFrame, col_1:str, col_2:str) -> pd.DataFrame:
    '''Calculate the percent difference between the total of two data
    series added together and each series
    '''
    df_out = pd.DataFrame()

    # Copy id column from incoming dataframe to outgoing dataframe
    df_out['id']= df_in['id']

    # Set the df index to the id column
    df_out.set_index('id')

    # Copy the incoming data-series to the outgoing dataframe
    df_out[col_1] = df_in[col_1]
    df_out[col_2] = df_in[col_2]

    # Calculate the percent difference
    df_out['percent_diff'] = (df_in[col_1] - df_in[col_2]) / (df_in[col_1] + df_in[col_2])

    return df_out


'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    from ccat import Bucket

    # Get a bucket object from Bucket
    b = Bucket(market_id=1,timeframe_id=1)

    # Update the table
    b.update()

    # Get a dataframe with all the data for the market and timeframe
    df_in = b.read_all()

    # Calculate the heights
    w = height(df_in)
    print(w)

    # Calculate the diff


    # Calculate the % diff



