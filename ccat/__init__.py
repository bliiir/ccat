'''
------------------------------------------------------------------------
    __INIT__.PY
------------------------------------------------------------------------
Package constructor for CCAT:
[C]rypto [C]urrency [A]uto [T]rader - pronounced [see-cat]
'''

name = 'ccat'

'''
------------------------------------------------------------------------
    MODEL
------------------------------------------------------------------------
'''

import ccat.model.engine as engine
import ccat.model.exchange as exchange
import ccat.model.bucket as bucket

'''
------------------------------------------------------------------------
    CONTROLLER
------------------------------------------------------------------------
'''

# Features
import ccat.controller.feature.height as height
import ccat.controller.feature.diff as diff

# Indicators
import ccat.controller.indicator.ema as ema
import ccat.controller.indicator.sma as sma
import ccat.controller.indicator.rsi as rsi

# Cross
import ccat.controller.cross.df_x_df as df_x_df
import ccat.controller.cross.df_x_val as df_x_val



# # Strategies
# #import ccat.controller.strategy.s_1542995464 as s2

# # Views
# from ccat.view import report

