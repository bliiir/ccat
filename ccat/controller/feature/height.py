# IMPORTS --------------------------------------------------------------

# Standard library imports
import pdb

# Third party imports
import pandas as pd
import numpy as np

# Local application imports
from ccat import config


# FEATURE --------------------------------------------------------------

def get(
    df_in: pd.DataFrame) -> pd.DataFrame:

    cols = [
        'id',           # 0
        'abs_total',    # 1
        'abs_body',     # 2
        'abs_top',      # 3
        'abs_bottom',   # 4
        'pct_body',     # 5
        'pct_top',      # 6
        'pct_bottom']   # 7


    '''Calculates the absolute (abs) and relative (pct) height of the
    candle and its elements - total, body, top-wick and bottom-wick

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
                Absolute difference between the price_high and
                price_low denominated in the quota asset,

            height_body:
                Absolute difference between the price_close and
                price_open denominated in the quota asset,

            height_top:
                Absolute difference between the price_close (if higher than
                price_open, and price_open if not) and price_high
                denominated in the quota asset,

            height_bottom:
                Absolute difference between the price_close (if lower than
                price_open, and price_open if not) and price_high
                denominated in the quota asset,

            percent_body:
                Relative height of the body to the total
                height_body/height_total

            percent_top:
                Relative height of the top wick to the total
                height_top/height_total,

            percent_bottom:
                Relative height of the bottom wick to the total
                height_bottom/height_total
    '''

    df_out = pd.DataFrame()

    # Copy id column from incoming dataframe to outgoing dataframe
    df_out[cols[0]]= df_in[cols[0]].copy()

    # Set the df index to the id column
    df_out.set_index(cols[0])

    # Total height
    df_out[cols[1]] = df_in.price_high-df_in.price_low

    # Body height
    df_out[cols[2]] = df_in.price_close-df_in.price_open

    # Top wick height
    df_out[cols[3]]=np.where(
        df_in.price_close >= df_in.price_open,
        df_in.price_high - df_in.price_close,
        df_in.price_high - df_in.price_open)

    # Bottom wick height
    df_out[cols[4]]=np.where(
        df_in.price_close < df_in.price_open,
        df_in.price_close - df_in.price_low ,
        df_in.price_open - df_in.price_low)

    # Body height percentage of total candle height
    df_out[cols[5]] = df_out[cols[2]] / df_out[cols[1]]

    # Top Wick height percentage of total candle height
    df_out[cols[6]] = df_out[cols[3]] / df_out[cols[1]]

    # Bottom Wick height percentage of total candle height
    df_out[cols[7]] = df_out[cols[4]] / df_out[cols[1]]

    return df_out
