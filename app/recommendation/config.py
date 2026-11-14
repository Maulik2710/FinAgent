# ----------------------------
# Forecast thresholds
# ----------------------------
# The forecast is a NEXT-DAY expected return, and daily moves are small:
# +-5% (the old value) would almost never trigger. +-0.5% is a realistic start.
BULLISH_THRESHOLD = 0.005
BEARISH_THRESHOLD = -0.005

# Text used in the explanation ("... expected next-day move")
FORECAST_HORIZON_LABEL = "next-day"

# ----------------------------
# News sentiment thresholds (score is between -1 and +1)
# ----------------------------
POSITIVE_SENTIMENT = 0.20
NEGATIVE_SENTIMENT = -0.20

# ----------------------------
# Portfolio allocation thresholds (share of the optimized portfolio)
# ----------------------------
HIGH_ALLOCATION = 0.15
LOW_ALLOCATION = 0.05

# ----------------------------
# Weights for each module
# ----------------------------
FORECAST_WEIGHT = 0.5
NEWS_WEIGHT = 0.3
PORTFOLIO_WEIGHT = 0.2

# ----------------------------
# Final score -> action
# ----------------------------
# Score runs from -1 to +1. With the weights above, news alone (0.3) or the
# portfolio alone (0.2) can NOT trigger a Buy/Sell; the forecast alone (0.5)
# or any two agreeing signals can. Strong Buy/Sell needs forecast + news.
BUY_SCORE = 0.4
STRONG_BUY_SCORE = 0.8

DISCLAIMER = (
    "This is an automated, educational analysis and not financial advice."
)