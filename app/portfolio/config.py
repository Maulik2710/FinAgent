# Number of trading days in one year
TRADING_DAYS = 252

# Annual risk-free rate (approximate). Update it to the current T-bill / bond yield.
RISK_FREE_RATE = 0.05

# Maximum share of the portfolio any single stock may get.
# Without a cap, optimizers pile everything into the best past performer
# (e.g. 80% NVDA). 0.30 = at most 30% per stock.
MAX_WEIGHT = 0.30

# Use only the most recent N trading days to estimate returns and risk
# (1260 ~ 5 years). Old history says little about today. None = use everything.
LOOKBACK_DAYS = 1260

# Minimum number of common trading days required to trust the statistics
MIN_OBSERVATIONS = 250

# Weights below this are treated as 0 (removes optimizer noise like 1e-17)
MIN_WEIGHT = 1e-4