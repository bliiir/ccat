'''
------------------------------------------------------------------------
    TABLE.PY
------------------------------------------------------------------------
Tables of relevant data
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
import ccat.model.bucket as bucket
import ccat.controller.feature as feature
import ccat.controller.indicator as indicator
import ccat.config as cf


'''
------------------------------------------------------------------------
    CLASSES
------------------------------------------------------------------------
'''
class Report():
    '''Common tables I want to check all the time
    - like price and indicators together


    '''

    def __init__(
        self,
        market_id = 1,
        timeframe_id = 1,
        count = 100,
        time_begin = cf.month_ago(),
        time_end = cf.now()):

        '''Constructor for the Report class. Takes arguments and creates
        A new bucket object with them and then reads a dataframe with
        bucket data between two dates defined by the arguments

        '''

        self.market_id = market_id
        self.timeframe_id = timeframe_id
        self.count = count
        self.time_begin = time_begin
        self.time_end = time_end


        # Createa a bucket object
        self.bucket = bucket.Bucket(
            market_id=self.market_id,
            timeframe_id=self.timeframe_id)

        # Update the bucket - PUT THIS IN A SEPARATE SCHEDULER INSTEAD!!
        # self.bucket.update()

        # Read bucket data into a dataframe from the database
        self.df_bucket = self.bucket.read_between(time_begin, time_end)

        # Calculate the height features
        self.df_height = feature.height(self.df_bucket)

    # SMA
    def indicator_sma(
        self,
        n=12,
        _id='id',
        data='price_close',
        prefix='price_close'):

        self.df_sma = indicator.sma(
            df_in = self.df_bucket,
            id = _id,
            data = data,
            n = n,
            prefix = prefix)

        return self.df_sma


    # EMA
    def indicator_ema(
        self,
        n=12,
        _id='id',
        data='price_close',
        prefix='price_close'):

        self.df_ema = indicator.ema(
                df_in = self.df_bucket,
                n = n,
                id = _id,
                data = data,
                prefix = prefix )

        return self.df_ema

    # RSI
    def indicator_rsi(
        self,
        n=12,
        _id='id',
        data='price_close',
        prefix='price_close'):

        self.df_rsi = indicator.rsi(
                df_in = self.df_bucket,
                n = n,
                id = _id,
                data = data,
                prefix = prefix )

        return self.df_rsi

    # Merge two dataframes
    def merge(self, df_left, df_right):
        df_out = pd.merge(df_left, df_right, how='left', left_on='id', right_on='id',)
        return df_out


    # Return a full report
    def report(self):
        '''Returns a full report with all the indicators
        '''

        # Clean dataframe
        df_out = pd.DataFrame()

        # Get the bucket data
        df_out = self.df_bucket
        df_out.set_index('id')
        print(df_out)
        print(self.df_height)

        # # Add heights to the bucket data
        df_out = pd.merge(df_out, self.df_height, how='left', left_on='id', right_on='id',)

        # Define the lookback - ie how many candles to indclude in the
        # sma, ema, rsi etc calculations
        timeframes = [4, 8, 16, 32, 64, 128, 256]

        # Loop through the timeframes and add indicators for each to df_out
        for timeframe in timeframes:

            # Join indicators to df_out
            df_out = pd.merge(df_out, self.indicator_sma(n=timeframe), how='left', left_on='id', right_on='id',)
            df_out = pd.merge(df_out, self.indicator_ema(n=timeframe), how='left', left_on='id', right_on='id',)
            df_out = pd.merge(df_out, self.indicator_rsi(n=timeframe), how='left', left_on='id', right_on='id',)

        return df_out


'''
------------------------------------------------------------------------
    FUNCTIONS
------------------------------------------------------------------------
'''
pass



'''
------------------------------------------------------------------------
    __MAIN__
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    my_report = Report()
    print(my_report.report()[300:350])
