# IMPORTS --------------------------------------------------------------

# Standard library imports
import pdb

# Third party imports
import pandas as pd
import numpy as np

# Local application imports
from ccat import config
import ccat.controller.feature.height as height
import ccat.controller.indicator.ema as ema
import ccat.controller.helper.df_x_df as df_x_df
import ccat.controller.helper.df_magic as df_magic



# SIGNAL --------------------------------------------------------------

class Reversal:
    '''Signals long (1) or short (-1) or no action (0) based on
    crossovers of wick height ema crosses
    '''

    def __init__(
        self,
        df_bucket:pd.DataFrame,
        len_ma_top:int = 40,
        len_ma_bottom:int = 40,
        prefix = 'reversal'):

        # self.df_bucket = df_bucket
        # self.len_ma_top = len_ma_top
        # self.len_ma_bottom = len_ma_bottom
        self.prefix = prefix

        # Get the candle heights
        df_heights = height.get(df_bucket)

        # Get the top wick ema's
        df_ema_top = ema.get(
            df_in = df_heights,
            id = 'id',
            data = 'abs_top',
            n = len_ma_top,
            prefix = f'{prefix}_abs_top')

        # Get the bottom wick ema's
        df_ema_bottom = ema.get(
            df_in = df_heights,
            id = 'id',
            data = 'abs_bottom',
            n = len_ma_bottom,
            prefix = f'{prefix}_abs_bottom')

        # Get the top and bottom wick ema crossovers
        self.df_x = df_x_df.get(
            df_in_1 = df_ema_top,
            df_in_2 = df_ema_bottom,
            col_1 = f'{prefix}_abs_top_ema',  # ?
            col_2 = f'{prefix}_abs_bottom_ema',
            prefix = prefix)  # ?


    def long(self):

        # Copy the id and {}_crossover columns from the df_x dataframe
        df = self.df_x[['id', f'{self.prefix}_crossover']].copy() ## ONLY COPY THE RELEVANT COLS

        # Calculate the long signal
        df[f'{self.prefix}_long'] = np.where(
            df[f'{self.prefix}_crossover'],  ## The long signal is issued when the top-wick ema crosses OVER the bottom wick. It was supposed to be the other way around
            1,
            0)

        return df[['id', f'{self.prefix}_long']]


    def short(self):

        # Copy the df_x dataframe
        df = self.df_x[['id', f'{self.prefix}_crossunder']].copy() ## ONLY COPY THE RELEVANT COLS

        # Calculate the short signal
        df[f'{self.prefix}_short'] = np.where(
            df[f'{self.prefix}_crossunder'],
            -1,
            0)

        return df[['id', f'{self.prefix}_short']]


    def get(
        self,
        cols:list = None,
        rows:int = None) -> pd.DataFrame:
        '''If the top wick ema crosses over the bottom wick ema, return
        a 1 (long), if the top wick crosses under the bottom wick ema,
        return a -1(short), otherwise return a 0 (do nothing)

        Args:
            self(obj):

            cols (list):
                list of columns to include in returned dataframe.
                Options:

            :rows (int):
                An integer indicating a number of rows to return
                counting from the end of the dataframe

        Returns:
            :df (pandas.DataFrame):
                A pandas dataframe with the columns listed in cols and
                number of rows indicated with rows
        '''

        # # Merge the dataframes in the dfs list
        df = pd.merge(self.long(), self.short())

        # Add a signal column with the sum of overbought and oversold
        df[f'{self.prefix}_signal'] = np.where(
            df[f'{self.prefix}_long'], 1,
            np.where(
                df[f'{self.prefix}_short'], -1,
            0))

        # Crop the df dataframe to just the columns in cols
        df = df_magic.crop(df, cols = cols, rows = rows)

        return df


    def signal(self):
        '''Returns only the last signal in the dataframe
        '''

        # Get a dataframe with only the signal column and last row
        df = self.get(cols=[f'{self.prefix}_signal'], rows = 1)

        # Extract the signal
        signal = int(df[f'{self.prefix}_signal'].values[0])

        return signal
