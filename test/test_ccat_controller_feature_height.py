'''
------------------------------------------------------------------------
    IMPORTS
------------------------------------------------------------------------
'''

# Standard packages
import unittest

# Third party packages
pass

# Local packages
from ccat.model.database.bucket import Bucket
import ccat.controller.feature.height as height


'''
------------------------------------------------------------------------
    CLASSES
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

        self.assertCountEqual(
            list(self.df_out.columns.values),
            col_names)




'''
------------------------------------------------------------------------
    MAIN
------------------------------------------------------------------------
'''

if __name__ == '__main__':

    unittest.main()