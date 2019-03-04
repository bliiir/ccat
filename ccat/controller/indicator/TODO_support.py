# Levels

# // Feature
# candle_top = open > close ? open:close
# candle_bottom = open < close ? open:close
# candle_green = open < close
# candle_red = open > close



# resistance_move_down = high/tolerance_resistance < open[3]
# resistance := candle_green[3] and candle_red[2] and resistance_move_down ? close[3] : resistance[1]
# resistance_unbroken = high < resistance and candle_top[1] < resistance
# resistance := resistance_unbroken ? resistance : na
# // resistance_broken = low > resistance

# long = low > support
# short = high < resistance



# # Support
# support_move_up = low * tolerance_support > close[3]
# support := candle_red[3] and candle_green[2] and support_move_up ? close[3] : support[1]
# support_unbroken = low > support and candle_bottom[1] > support
# support := support_unbroken ? support : na
# // support_broken = high < support
