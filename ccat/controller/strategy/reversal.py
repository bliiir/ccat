# IMPORTS --------------------------------------------------------------

# Standard library imports
import pdb
# from datetime import datetime as dt

# Third party imports
import pandas as pd
import numpy as np


# Local application imports
from ccat.controller.helper import time as t
import ccat.controller.feature.height as height
import ccat.controller.indicator.ema as ema
import ccat.controller.helper.df_x_df as df_x_df

from ccat.controller.helper import df_magic

from ccat.controller.signal.reversal import Reversal


# STRATEGY --------------------------------------------------------------

class Strategy:
    '''
    This strategy is based on the reversal indicator

    REVERSAL
    Consider the length of the candle wicks to be indicators of reversals.
    I calculate an ema for the length of the top and the bottom wicks.
    If they cross eachother, a buy/sell signal is returned

        long = ema(height_bottom, len) > ema(height_top, len)
        short = ema(height_bottom, len) > ema(height_top, len)


    '''

    def __init__(
        self,
        df_bucket:pd.DataFrame,
        **kwargs):
        '''Initialize the strategy

        Argumentss:
            df_bucket(pd.DataFrame);
                Pandas dataframe with the raw timeseries data

            **kwargs(dict):
                Keyword arguments relating to the specifics of the
                strategy
        '''

        self.df_bucket = df_bucket
        self.kwargs = kwargs


    def source(self):
        '''Add the data that the signals are derived from
        '''

        # Get the datetime
        df_datetime = t.unix_to_datetime(
            df = self.df_bucket,
            col = self.df_bucket.columns[4])

        # Get the feature dataframes
        df_heights = height.get(self.df_bucket)

        # Get the indicator dataframes

        # ## REVERSAL
        df_ema_top_reversal = ema.get(
            df_in = df_heights,
            id = 'id',
            data = df_heights.columns[3],
            n = self.kwargs['len_ma_top'],
            prefix = (
                f"{self.kwargs['prefix']}_"
                f"{df_heights.columns[3]}_"
                f"{self.kwargs['len_ma_top']}"))

        df_ema_bottom_reversal = ema.get(
            df_in = df_heights,
            id = 'id',
            data = df_heights.columns[4],
            n = self.kwargs['len_ma_bottom'],
            prefix = (
                f"{self.kwargs['prefix']}_"
                f"{df_heights.columns[4]}_"
                f"{self.kwargs['len_ma_bottom']}")
            )

        df_x_wick_ema_reversal = df_x_df.get(
            df_in_1 = df_ema_top_reversal,
            df_in_2 = df_ema_bottom_reversal,
            col_1 = df_ema_top_reversal.columns[1],
            col_2 = df_ema_bottom_reversal.columns[1],
            prefix = self.kwargs['prefix'])

        # Merge
        dfs = [
            df_datetime,
            self.df_bucket,
            df_heights,
            df_ema_top_reversal,
            df_ema_bottom_reversal,
            df_x_wick_ema_reversal]

        # # Merge the dataframes
        df = df_magic.merge(dfs = dfs, on = 'id')

        return df


    def signals(
        self,
        src:bool = False,
        cols:list = None,
        rows: int = None):
        '''Triggers the chain of methods and returns the df_signals
        dataframe

        Needs the following arguments as part of the kwargs:
            reversal_len_ma_top
            reversal_len_ma_bottom
            reversal_prefix
        '''

        # Create an instance of the strategy
        strategy = Reversal(
            df_bucket = self.df_bucket,
            len_ma_top = self.kwargs['len_ma_top'],
            len_ma_bottom = self.kwargs['len_ma_bottom'],
            prefix = self.kwargs['prefix'])

        # Run the strategy on the provided dataframe
        df = strategy.get()

        # Get source data if flag set to True
        if src == True:

            # Get the source data
            source = self.source()

            # Merge the dataframes
            df = df_magic.merge([df, source], on = 'id')

        # Crop the dataframe
        df = df_magic.crop(df, cols=cols, rows=rows)

        return df


    def signal(self):
        '''Returns only the signal of the last frame of the signals
        '''

        col = f"{self.kwargs['prefix']}_signal"

        df = self.signals(
            rows = 1,
            cols = [col])

        signal = int(df[col].tail(1).values[0])

        return signal

