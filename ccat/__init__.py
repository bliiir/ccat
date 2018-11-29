# CCAT: [C]rypto [C]urrency [A]uto [T]rader - pronounced [see-cat]
name = 'ccat'


# # Config
# import ccat.config as config

# # Models
# import ccat.model.bucket as bucket
# from ccat.model.engine import Sql_engine

# make the engine module available in all other files so that we can use
# for example engine.Sql_engine(...) instead of
# ccat.model.engine.Sql_engine(...)
# import ccat.model.engine as engine


# import ccat.model.exchange as exchange
from ccat.model.engine import Sql_engine
from ccat.model.exchange import Exchange
from ccat.model.bucket import Bucket
from ccat.model import bucket


# # Controllers
import ccat.controller.feature as feature
import ccat.controller.indicator as indicator
import ccat.controller.signal as signal

# # Strategies
# #import ccat.controller.strategy.s_1542995464 as s2

# # Views
from ccat.view import report

