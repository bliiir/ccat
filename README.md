# Bit crypto trading platform
Lorem ipsum

## Project structure

lib/
	model/
		Modules for doing I/O operations on  the platform. Classes, methods
		and functions to aqcuire, store and retreive data from exchange api's,
		the Postgres database etc.

			[exchange.py]
			[database.py]

	view/
		Modules for presenting data to users - including classes, methods
		and functions to present data to a privilliged user and classes,
		methods and functions to present data via the api and the website

			{indicators.py} 	Shows the indicators and their current status
			{signals.py} 		Shows the signals and their current status
			{strategy.py} 		Shows the strategies, their current status
								and historical performance
			{dashboard.py} 		Shows the equity curve for each bot and the total

	controller/
		Modules for processing data. This is where all the features,
		indicators, signals, strategies and bots will live

			(feature.py)

			(indicator.py)

			(signal.py)

				crossover()
				crossunder()

			[strategy.py]
				Monitors signals and initates trades when the strategy
				criteria is me

			[executor.py]
				executes trades using the following abstract functions mirroring the same methods in the Exchange module

					limit_order()
					limit_stop_loss()
					limit_take_profit()
					limit_trailing_stop

					market_order()
					market_stop_loss()
					market_take_profit()
					market_trailing_stop()


			{manager.py}
				The manager module enforces money-management policies.
				For example daily rebalancing of capital on each exchange,
				allocations to different buckets - like hodl, invest, trade

					{rebalance()}


BIT crypto trading platform
