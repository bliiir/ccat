# Crypto Currency Auto Trader
Last updated: (2019, 01, 25)

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

| File | Status | Purpose |
| :-- | :-- | :-- |
| client.py | current | The database connection. Uses SQLalchemy so can be most popular databases |
| bucket.py | current | The candle data connection |

#### exchange

| File | Status | Purpose |
| :-- | :-- | :-- |
| engine.py | current | The database connection |
| exchange.py | current | The Exchange connection |
| bucket.py | current | The candle data connection |


---

### view
Modules for presenting data to users - including classes, methods and functions to present data to a privilliged user and classes, methods and functions to present data via the api and the website

| File | Status | Purpose |
| :-- | :-- | :-- |
| indicators.py | not started | Shows the indicators and their current status |
| signals.py | not started | Shows the signals and their current status |
| strategy.py | not started | Shows the strategies, their current status and historical performance |
| dashboard.py | not started| Shows the equity curve for each bot and the total |

---

### controller
Modules for processing data. This is where all the features, indicators, signals, strategies and bots will live

#### feature
Extracts simple features from the raw data - for example the difference between the open and close price or the height of the wicks

| File | Status | Purpose |
| :-- | :-- | :-- |
| diff.py | current | Calculate the difference between two columns in a pandas dataframe |
| height.py | current | Calculate the height of the candle body, top and bottom wicks |

#### indicator
Calculations on top of the raw data and features - for example the RSI, Relative Strength Index

| File | Status | Purpose |
| :-- | :-- | :-- |
| ema.py | current | Calculate the Exponential Moving Average using a pandas dataframe |
| rsi.py | current | Calculate the Relative Strength Index using a pandas dataframe |
| sma.py | current | Calculate the Simple Moving Average using a pandas dataframe |
| support.py | deprecated | Calculate support and resistance levels using a pandas dataframe |

#### cross
Indicator Crossovers

| File | Status | Purpose |
| :-- | :-- | :-- |
| df_x_df.py | current | Calculate crossover of values of two columns in two dataframes |
| df_x_val.py | current |  Calculate crossover of values in a pandas dataframe column and a fixed value |

#### signal
Trading signals. I do not publish all signals for obvious reasons

| File | Status | Purpose |
| :-- | :-- | :-- |
| extreme.py | current | Signal extreme overtrading |
| overtraded.py | current | Signal traditional RSI overtrading |
| wix.py | current | Signal overtrading based on wicks |


#### strategy
Monitors signals and initates trades when the strategy criteria is met. I do not publish all signals for obvious reasons

| File | Status | Purpose |
| :-- | :-- | :-- |
| template.py | not started | Give other trader-devs a template strategy to work from |


#### order
Executes trades using the following abstract functions mirroring the same methods in the Exchange module

| File | Status | Purpose |
| :-- | :-- | :-- |
| order.py | not started | Place an order on the exchange |
| stop_loss.py | not started | Stop loss monitor that executes an order when conditions are met |
| take_profit.py | not started | Take-profit monitor that executes an order when conditions are met |
| trailing_stop.py | not started | Monitor that executes an order when conditions are met |


### manager
The manager module enforces money-management policies. For example daily rebalancing of capital on each exchange, allocations to different buckets - like hodl, invest, trade

| File | Status | Purpose |
| :-- | :-- | :-- |
| rebalance.py | not started | Rebalance the portfolio across assets, pools and exchanges |
