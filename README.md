# Crypto Currency Auto Trader
Last updated: (2019, 03, 08)

#### URLS

| File | Status | Purpose |
| :-- | :-- | :-- |
| [Github](https://github.com/bliiir/ccat) | current | Project home |
| [pypi](https://pypi.org/project/ccat/) | needs updating | Pip install source |

---

## ccat

---

### model
Modules for doing I/O operations on the platform. Classes, methods and functions to aqcuire, store and retreive data from exchange api's, the Postgres database etc.

#### database
Home-made interaction layer with the database - ORM would be too big a word, but sort of like it


#### exchange
Interactions with the exchanges - fetch candles, place and check orders etc


---

### view
Modules for presenting data to users - including classes, methods and functions to present data to a privilliged user and classes, methods and functions to present data via the api and the website

Nothing here yet

---

### controller
Modules for processing data. This is where all the features, indicators, signals, strategies and bots will live

#### feature
Extracts simple features from the raw data - for example the difference between the open and close price or the height of the wicks


#### indicator
Calculations on top of the raw data and features - for example the RSI, Relative Strength Index


#### helper
Helper modules - crop and merge dataframes, calculate crossovers etc



#### signal
Trading signals. I do not publish all signals for obvious reasons


#### strategy
Monitors signals and initates trades when the strategy criteria is met. I do not publish all signals for obvious reasons


#### order
Executes trades using the following abstract functions mirroring the same methods in the Exchange module


### manager
The manager module enforces money-management policies. For example daily rebalancing of capital on each exchange, allocations to different buckets - like hodl, invest, trade

Nothing here yet
