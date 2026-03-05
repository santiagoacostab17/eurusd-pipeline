instrument {
  name ="candle_pattern",
  icon='indicators:ADX',
  overlay = " true"
}
      color_white = "white"
      color_resistance = "red"
      color_support = "green"
      if close[1] > high[2] and high[1] - close[1] < close[1] - open[1] then support_signal = open[1] end
      if close[1] < low[2] and close[1] - low[1] < open[1] - close[1] then resistance_signal = open[1] end
      hline(resistance_signal, "Resistance", color_resistance, width)
      hline(support_signal, "Support", color_support, width)

