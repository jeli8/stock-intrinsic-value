# File paths
CSV_FILE = "tickers.csv"

# Default DCF parameters
DEFAULT_GROWTH_RATE = 0.05
DEFAULT_DISCOUNT_RATE = 0.10
DEFAULT_YEARS = 5
DEFAULT_TERMINAL_GROWTH = 0.02

# Trading thresholds
VALUATION_THRESHOLD = 0.20  # 20% threshold for strong buy/sell signals
UNDERVALUED_STOP_LOSS_PCT = 0.10  # 10% below entry for buy signals
UNDERVALUED_PROFIT_TARGET_INTRINSIC_PCT = 0.10  # 10% above intrinsic value
UNDERVALUED_PROFIT_TARGET_PRICE_PCT = 0.30  # 30% above entry price
OVERVALUED_STOP_LOSS_PCT = 0.05  # 5% below current for sell signals
OVERVALUED_PROFIT_TARGET_PCT = 0.05  # 5% above current for sell signals
FAIR_VALUE_STOP_LOSS_PCT = 0.10  # 10% below intrinsic for hold signals
FAIR_VALUE_PROFIT_TARGET_PCT = 0.10  # 10% above intrinsic for hold signals
