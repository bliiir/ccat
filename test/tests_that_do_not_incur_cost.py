'''
------------------------------------------------------------------------
    TEST.PY
------------------------------------------------------------------------
Calculates the heights of the different parts of the candles
# https://docs.python.org/3.7/library/unittest.html#module-unittest
'''


'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest
from datetime import datetime as dt
# import inspect

# Third party packages
import pandas as pd
import numpy as np
import sqlalchemy

# Local packages
from ccat import config

from ccat.model.database.bucket import Bucket
from ccat.model.database.client import Client
from ccat.model.database.instrument import Instrument
from ccat.model.database.market import Market
from ccat.model.database.timeframe import Timeframe

from ccat.model.exchange.exchange import Exchange
from ccat.model.exchange.order import Order

import ccat.controller.feature.height as height

import ccat.controller.indicator.ema as ema
import ccat.controller.indicator.rsi as rsi
import ccat.controller.indicator.sma as sma

import ccat.controller.helper.df_crop as df_crop
import ccat.controller.helper.df_x_df as df_x_df
import ccat.controller.helper.df_x_val as df_x_val

from ccat.controller.signal.overtraded import Overtraded
from ccat.controller.signal.reversal import Reversal


'''
########################################################################
    CONTROLLER
########################################################################
'''

'''
------------------------------------------------------------------------
    SIGNAL
------------------------------------------------------------------------
'''

class Test_controller_signal_reversal_real_data(unittest.TestCase):
    '''Test if the overtraded module returns the expexted results by
    exposing it to a known dataset
    '''

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_bucket = cls.b.read_all()

        # Number of candles/buckets to include in the rsi calculation
        len_rsi = 20

        # Get an instance of the Overtraded object
        cls.reversal = Reversal(
            df_bucket = cls.df_bucket,
            len_ma_top = 40,
            len_ma_bottom = 40,
            suffix = 'wix')


    def test_reversal_get_custom(self):

        cols = [
            'id',
            'signal_wix']

        # print('\n', self.reversal.get(cols=my_cols))
        self.assertCountEqual(cols, self.reversal.get(cols).columns)
        self.assertEqual(10, len(self.reversal.get(cols).head(10)))


    def test_reversal_get_default(self):

        cols = [
            'id',
            'abs_top_ema',
            'abs_bottom_ema',
            'crossover',
            'crossunder',
            'cross',
            'long_wix',
            'short_wix',
            'signal_wix']

        # print('\n', self.reversal.get())
        self.assertCountEqual(cols, self.reversal.get().columns)
        self.assertEqual(10, len(self.reversal.get().head(10)))


    def test_reversal_object_has_time_series_data(self):

        cols = [
            'id',
            'market_id',
            'timeframe_id',
            'time_open',
            'time_close',
            'time_updated',
            'price_open',
            'price_high',
            'price_close',
            'price_low',
            'volume',
            'time_close_dt']

        # print(self.reversal.df_bucket.columns)
        self.assertIn('id', self.reversal.df_bucket.columns)
        self.assertCountEqual(cols, self.reversal.df_bucket.columns)
        self.assertEqual(10, len(self.reversal.df_bucket.tail(10)))


    def test_reversal_object_has_vars(self):
        # print(vars(self.reversal))
        self.assertIn('len_ma_top', vars(self.reversal))
        self.assertIn('len_ma_bottom', vars(self.reversal))


    def test_reversal_object_has_get_method(self):
        self.assertIn('get', dir(self.reversal))


class Test_controller_signal_overtraded_real_data(unittest.TestCase):
    '''Test if the overtraded module returns the expexted results by
    exposing it to a known dataset
    '''

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_bucket = cls.b.read_all()

        # Number of candles/buckets to include in the rsi calculation
        len_rsi = 20

        # Get an instance of the Overtraded object
        cls.overtraded = Overtraded(
            df_bucket = cls.df_bucket,
            len_rsi = len_rsi,
            high = 60,
            low = 40,
            col = 'price_close',
            suffix = 'rsi')

    def test_overtraded_get_custom(self):

        cols = [
            'id',
            'time_close_dt',
            'price_close',
            #'price_close_rsi',
            'signal_rsi']

        df = self.overtraded.get(cols = cols)

        # print('\n', df.tail(50))
        # print('\n', df.to_string())
        self.assertEqual(len(df.columns), len(cols))
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_get_default(self):
        df = self.overtraded.get()
        # print('\n', df.to_string())
        # print('\n', df.tail(50))
        self.assertGreater(len(df.columns), 2)
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_overbought(self):
        df = self.overtraded.overbought()
        # print('\n', df.tail(50))
        # print('\n', df.to_string())
        self.assertEqual(len(df.columns), 3)
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_oversold(self):
        df = self.overtraded.oversold()
        # print('\n', df.tail(50))
        # print('\n', df.to_string())
        self.assertEqual(len(df.columns), 3)
        self.assertEqual(len(df.head(10)), 10)


class Test_controller_signal_overtraded_fake_data(unittest.TestCase):
    '''Test if the overtraded module returns the expexted results by
    exposing it to a known dataset
    '''

    @classmethod
    def setUpClass(cls):

        # Number of candles/buckets to include in the rsi calculation
        len_rsi = 20

        # Generate fake data
        x = np.arange(0, 10, 0.1)
        y = (np.sin(x) + 1)/2 *1000

        # Create a dataframe with the fake data
        df = pd.DataFrame({'price_close':y})

        # Set id column = index and then as the id column for merging
        df['id'] = df.index
        df = df[['id', 'price_close']]

        # Get an instance of the Overtraded object
        cls.overtraded = Overtraded(
            df_bucket = df,
            len_rsi = len_rsi,
            high = 60,
            low = 40,
            col = 'price_close',
            suffix = 'rsi')

    def test_overtraded_get(self):

        cols = [
            'id',
            'price_close',
            'price_close_rsi',
            'long_rsi',
            'short_rsi',
            'signal_rsi'
            ]

        df = self.overtraded.get([cols[1], cols[2], cols[5]])
        # print('\n', df.to_string())
        print('\n', df.head())
        self.assertEqual(len(df.columns), 4)
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_get_default(self):
        df = self.overtraded.get()
        # print('\n', df.to_string())
        self.assertGreater(len(df.columns), 2)
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_overbought(self):
        df = self.overtraded.overbought()
        # print('\n', df.to_string())
        self.assertEqual(len(df.columns), 3)
        self.assertEqual(len(df.head(10)), 10)

    def test_overtraded_oversold(self):
        df = self.overtraded.oversold()
        # print('\n', df.to_string())
        self.assertEqual(len(df.columns), 3)
        self.assertEqual(len(df.head(10)), 10)


class Test_controller_signal_overtraded_basics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Variables
        market_id = 1
        timeframe_id = 6
        time_end=config.now()
        count = 500
        len_rsi = 40
        col = 'price_close'
        high = 60
        low = 40
        # peak = 92
        # trough = 32

        # Read candle data
        bucket = Bucket(
            market_id=market_id,
            timeframe_id=timeframe_id)

        cls.df_bucket = bucket.read_until(
            count = count,
            time_end = time_end)

        cls.overtraded = Overtraded(
            df_bucket = cls.df_bucket,
            len_rsi = len_rsi,
            high = high,
            low = low,
            col = col)

        cls.signal = cls.overtraded.get()


    def test_overtraded_signal(self):

        self.df_bucket = pd.DataFrame(
            [
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),
            (1,100),

            ],
            columns = ['id', 'price_close'] )

    def test_overtraded_col_names(self):

        col_names = [
            'id',
            'market_id',
            'timeframe_id',
            'time_open',
            'time_close',
            'time_updated',
            'price_open',
            'price_high',
            'price_close',
            'price_low',
            'volume',
            'time_close_dt',
            'price_close_rsi',
            'long_rsi','short_rsi',
            'signal_rsi']

        # print('\nACTUAL COL NAMES: ', self.signal.columns.values)
        # print('ASSUMED COL NAMES: ', col_names)

        self.assertCountEqual(
            list(self.signal.columns.values),
            col_names)

    # def test_overtraded(self):
        # print('\n\nOVERTRADED: \n\n', self.signal)

    def test_overtraded_has_content(self):
        self.assertEqual(len(self.signal.tail(10)), 10)

    def test_overtraded_pandas_dataframe(self):
        self.assertIsInstance(self.signal, pd.DataFrame)

    def test_overtraded_not_none(self):
        self.assertIsNotNone(self.signal)




'''
------------------------------------------------------------------------
    HELPER
------------------------------------------------------------------------
'''

class Test_controller_helper_df_x_val(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()

        # Calculate price_close rsi
        cls.price_close_rsi = rsi.get(
            df_in = cls.df_in, id='id',
            data = 'price_close',
            n = 40,
            prefix = 'price_close')

        # print(price_close_rsi)
        cls.rsi_x_val = df_x_val.get(
            df_in = cls.price_close_rsi,
            col = cls.price_close_rsi.columns[1],
            val = 30)


    def test_df_x_val_column_names(self):

        col_names = [
            'id',
            'price_close_rsi',
            'x_value',
            'crossover',
            'crossunder',
            'cross']

        self.assertCountEqual(
            list(self.rsi_x_val.columns.values),
            col_names)


    def test_df_x_val_has_content(self):
        self.assertEqual(len(self.rsi_x_val.tail(10)), 10)





class Test_controller_helper_df_x_df(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()

        # Calculate the wicks
        cls.df_height = height.get(cls.df_in)

        # Calculate wick_top ema
        cls.wick_top_sma = sma.get(
            df_in=cls.df_height, id='id',
            data='abs_top',
            n=40,
            prefix='abs_top')

        # Calculate wick_bottom ema
        cls.wick_bottom_sma = sma.get(
            df_in=cls.df_height, id='id',
            data='abs_bottom',
            n=40,
            prefix='abs_bottom')

        cls.crossover_wick_ema = df_x_df.get(
            df_in_1 = cls.wick_top_sma,
            df_in_2 = cls.wick_bottom_sma,
            col_1 = cls.wick_top_sma.columns[1],
            col_2 = cls.wick_bottom_sma.columns[1])


    def test_df_x_df_column_names(self):

        col_names = [
            'id',
            'abs_top_sma',
            'abs_bottom_sma',
            'crossover',
            'crossunder',
            'cross']

        # print('\nTest_column_names')
        # print('ACTUAL COL NAMES: ', list(self.crossover_wick_ema.columns.values))
        # print('ASSUMED COL NAMES: ', col_names)

        self.assertCountEqual(list(self.crossover_wick_ema.columns.values), col_names)


    def test_df_x_df_not_empty(self):
        # print("\nLENGTH", len(self.crossover_wick_ema))
        self.assertGreater(len(self.crossover_wick_ema), 1)

    def test_df_x_df_pd_dataframe(self):
        self.assertIsInstance(self.crossover_wick_ema, pd.DataFrame)

    def test_df_x_df_not_none(self):
        self.assertIsNotNone(self.crossover_wick_ema)


class Test_controller_helper_df_crop(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(market_id = 1, timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()


    def test_df_column_names(self):

        # Calculate the diffs
         # = (cls.df_in, cls.df_in, 'price_open', 'price_close')

        # print(diffs.columns.values)

        col_names = [
            'id',
            'market_id',
            'timeframe_id',
            'time_open',
            'time_close',
            'time_close_dt',
            'time_updated',
            'price_open',
            'price_high',
            'price_close',
            'price_low',
            'volume']

        # print('\nTest_column_names')
        # print('ACTUAL COL NAMES: ', list(self.df_in.columns.values))
        # print('ASSUMED COL NAMES: ', col_names)

        self.assertCountEqual(list(self.df_in.columns.values),col_names)


    def test_df_crop(self):

        col_names = ['price_high', 'price_low']

        df_out = df_crop.crop(self.df_in, col_names)

        # print('\nTest_crop')
        # print('ACTUAL COL NAMES: ', list(df_out.columns.values))
        # print('ASSUMED COL NAMES: ', col_names)

        self.assertCountEqual(list(df_out.columns.values), col_names)
        # print(df_out)

'''
------------------------------------------------------------------------
    INDICATOR
------------------------------------------------------------------------
'''

class Test_controller_indicator_sma(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id=1,
            timeframe_id=1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()

        # Calculate the wicks
        # cls.df_height = height.get(cls.df_in)

        # Calculate price_close rsi
        cls.my_sma = sma.get(
            df_in=cls.df_in,
            id='id',
            data='price_close',
            n=12,
            prefix='price_close')

        # print(cls.my_sma)

    def test_sma_not_none(self):
        self.assertIsNotNone(self.my_sma)


class Test_controller_indicator_rsi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id=1,
            timeframe_id=1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()

        # Calculate the wicks
        # cls.df_height = height.get(cls.df_in)

        # Calculate price_close rsi
        cls.my_rsi = rsi.get(
            df_in=cls.df_in,
            id='id',
            data='price_close',
            n=12,
            prefix='price_close')

        # print(cls.my_rsi)

    def test_rsi_not_none(self):
        self.assertIsNotNone(self.my_rsi)



class Test_controller_indicator_ema(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()

        # Calculate the wicks
        # cls.df_height = height.get(cls.df_in)

        # Calculate wick_top ema
        cls.my_ema = ema.get(
            df_in=cls.df_in,
            id='id',
            data='price_close',
            n=12,
            prefix='price_close')

        # print(cls.my_ema)


    def test_ema_not_none(self):
        self.assertIsNotNone(self.my_ema)


    def test_is_pandas_dataframe(self):
        # print(self.my_ema)
        self.assertIsInstance(self.my_ema, pd.DataFrame)

    # def test_is_pandas_dataframe(self):
    #     print(self.my_ema)
    #     self.assertIsInstance(self.my_ema, pd.dataframe)


'''
------------------------------------------------------------------------
    FEATURE
------------------------------------------------------------------------
'''


class Test_controller_feature_height(unittest.TestCase):

    # print('CURRENT FRAME: ', inspect.currentframe())

    @classmethod
    def setUpClass(cls):

        # Get a bucket object from Bucket
        cls.b = Bucket(
            market_id = 1,
            timeframe_id = 1)

        # Get a dataframe with all the data for the market and timeframe
        cls.df_in = cls.b.read_all()

        # Calculate the heights
        cls.df_out = height.get(cls.df_in)



    def test_controller_feature_candle_column_names(self):

        col_names = [
        'id',
        'abs_total',
        'abs_body',
        'abs_top',
        'abs_bottom',
        'pct_body',
        'pct_top',
        'pct_bottom']

        # print('ACTUAL COL NAMES: ', list(self.df_out.columns.values))
        # print('ASSUMED COL NAMES: ', col_names)

        self.assertCountEqual(
            list(self.df_out.columns.values),
            col_names)



'''
########################################################################
    VIEW
########################################################################
'''
pass



'''
########################################################################
    MODEL
########################################################################
'''

class Test_model_exchange_order(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.my_order = Order(market_id=1)

        # self.test_id = '8a26a525-c6e6-f284-754c-7ebcf221ac7a'
        cls.test_id = '52b43253-03de-9cb8-7664-eaa6dae51d7e'

        cls.status_options = [
            'canceled',
            'open',
            'closed',
            'new',
            'partiallyfilled',
            'filled',
            'doneforday',
            'canceled',
            'pendingcancel',
            'pendingnew',
            'rejected',
            'expired',
            'stopped',
            'untriggered',
            'triggered']


    def test_str_(self):
        self.assertIn("order_status", self.my_order.__str__())


    def test_order_not_none(self):
        # print("\nORDER ID: ", self.my_order.internal_id)
        self.assertIsNotNone(self.my_order)


    def test_load_order_from_id(self):
        # test_id = '8a26a525-c6e6-f284-754c-7ebcf221ac7a'
        test_order = self.my_order.load(order_id = self.test_id)
        # print('\nLOAD ORDER FROM ID TEST: ', test_order)
        # print('\nLOAD ORDER FROM ID STATUS TEST: ', test_order.order_status.lower())
        self.assertIn(test_order.order_status.lower(), self.status_options)


    def test_load_order_from_self(self):

        # Load order from exchange based on known order id
        # to avoid having to use funds
        test_order1 = self.my_order.load(order_id = self.test_id)

        # Load order from exchange based on self.order_id
        test_order2 = test_order1.load()

        # print('\nLOAD ORDER TEST: ', test_order2)
        # print('\nLOAD ORDER STATUS TEST: ', test_order2.order_status.lower())
        self.assertIn(test_order2.order_status.lower(), self.status_options)


    def test_cancel_order_via_order_id(self):
        order = self.my_order.load(order_id = self.test_id)
        status = order.cancel()

        # print("\nCANCEL STATUS, ORDER ID: ", status)
        # ERROR: bitmex {"error":{"message":"Not Found","name":"HTTPError"}}
        self.assertIn('bitmex', status)



class Test_model_exchange_exchange(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.market_id = 1
        cls.market = Market(market_id = cls.market_id)

        # Get exchange_id from market_id
        cls.exchange_id = cls.market.get_exchange_id()

        # Create an exchange instance
        cls.exchange = Exchange(exchange_id = cls.exchange_id)

        # Get an exchange client
        cls.exchange_client = cls.exchange.client()


    def test_get_exchange(self):
        self.assertIsNotNone(self.exchange)

    def test_get_exchange_client(self):
        self.assertIsNotNone(self.exchange_client)

    def test_get_exchange_client_name(self):
        self.assertEqual(self.exchange.name, 'Bitmex')

    def test_get_exchange_client_url(self):
        self.assertEqual(self.exchange_client.urls['www'], 'https://www.bitmex.com')


    def test_get_candles(self):

        limit = 500

        # Fetch the 1h BTC candles
        candles = self.exchange_client.fetchOHLCV(
            'BTC/USD',
            '1h',
            limit=limit,
            since=self.exchange.client.parse8601 ('2018-11-5T00:00:00Z'))

        df = pd.DataFrame(candles)
        df.columns = ['time_close', 'price_open', 'price_high', 'price_low', 'price_close', 'volume' ]
        # print(df.tail(10))

        # Check the df is not empty
        self.assertIsNotNone(df)

        # Check that df is a dataframe
        self.assertIsInstance(df, pd.DataFrame)

        # Check length of dataframe
        self.assertTrue(len(df) == limit)



class Test_model_database_timeframe(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    # def test_print_vars(self):
    #     my_timeframe = Timeframe(timeframe_id=1)
    #     print(vars(my_timeframe))

    def test_1m_name(self):
        my_timeframe = Timeframe(timeframe_id=1)
        self.assertEqual(my_timeframe.get_name(), '1m')

    def test_1m_ms(self):
        my_timeframe = Timeframe(timeframe_id=1)
        self.assertEqual(my_timeframe.get_ms(), 60000)

    def test_1h_name(self):
        my_timeframe = Timeframe(timeframe_id=4)
        self.assertEqual(my_timeframe.get_name(), '1h')

    def test_1h_ms(self):
        my_timeframe = Timeframe(timeframe_id=4)
        self.assertEqual(my_timeframe.get_ms(), 3600000)


class Test_model_database_market(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.market_id = 1
        cls.market = Market(cls.market_id)

    def test_market_is_not_none(self):
        self.assertIsNotNone(self.market)

    def test_market_get(self):
        self.assertIsNotNone(self.market.get())

    def test_market_get_exchange_id(self):
        self.assertEqual(self.market.get_exchange_id(), 3)

    def test_market_symbol_native(self):
        self.assertEqual(self.market.symbol_native, 'XBTUSD')

    def test_market_symbol_ccxt(self):
        self.assertEqual(self.market.symbol_ccxt, 'BTC/USD')



class Test_model_database_instrument(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.market_id = 1
        cls.my_instrument = Instrument(market_id=1)

    # def test_print_vars(self):
    #     print(vars(self.my_instrument))

    def test_is_not_none(self):
        self.assertIsNotNone(self.my_instrument)

    def test_market_symbol_native(self):
        self.assertEqual(
            self.my_instrument.market_symbol_native,
            'XBTUSD')

    def test_market_symbol_ccxt(self):
        self.assertEqual(
            self.my_instrument.market_symbol_ccxt,
            'BTC/USD')

    def test_exchange_id(self):
        self.assertEqual(
            self.my_instrument.exchange_id,
            3)


class Test_model_database_bucket(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.market_id = 1
        cls.timeframe_id = 1

        cls.bucket = Bucket(
            market_id=cls.market_id,
            timeframe_id=cls.timeframe_id)

        # Update the table
        # cls.bucket.update()


    def test_model_database_bucket_instantiation(self):
        self.assertEqual(self.bucket.market_id, self.market_id)


    def test_model_database_bucket_update(self):
        self.buckets = self.bucket.update()
        # print('UPDATE: ', self.buckets)
        self.assertIsNotNone(self.buckets)

    def test_model_database_bucket_update_length(self):
        self.buckets = self.bucket.update(count=25)
        # print('LENGTH: ', self.buckets)
        self.assertEqual(len(self.buckets), 25)


    def test_model_database_bucket_read_all(self):
        self.all = self.bucket.read_all()
        # print('READ ALL: ', self.all)
        self.assertIsNotNone(self.all)


class Test_model_database_client(unittest.TestCase):

    def test_model_database_client_creation(self):

        db_engine = Client.get()

        self.assertIsInstance(db_engine, sqlalchemy.engine.base.Engine)


'''
########################################################################
    MAIN
########################################################################
'''

if __name__ == '__main__':

    unittest.main()