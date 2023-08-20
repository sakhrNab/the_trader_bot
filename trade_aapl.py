import yfinance as yf
import pandas as pd
from eventregistry import *

# Define Parameters
INITIAL_CAPITAL = 10000  # Example amount
LEVERAGE = 2  # 2:1 leverage
STOP_LOSS_PERCENTAGE = 0.02
TAKE_PROFIT_PERCENTAGE = 0.03
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# Fetch historical data for AAPL
data = yf.download('AAPL', period='1mo', interval='1d')
data['50_MA'] = data['Close'].rolling(window=50).mean()
data['200_MA'] = data['Close'].rolling(window=200).mean()

# Calculate RSI
delta = data['Close'].diff()
gain = (delta.where(delta > 0, 0)).fillna(0)
loss = (-delta.where(delta < 0, 0)).fillna(0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
data['RSI'] = 100 - (100 / (1 + rs))

# Initialize Event Registry
er = EventRegistry(apiKey="")

# Search for recent articles related to AAPL with positive sentiment
q = QueryArticlesIter(
    keywords="Apple Inc.",
    minSentiment=0.4,
    dataType=["news", "blog"])

significant_news = False
for art in q.execQuery(er, sortBy="date", maxItems=10):  # Check the last 10 articles
    if art['sentiment'] > 0.5:  # Example condition: High positive sentiment
        significant_news = True
        break

# Trading Algorithm
latest_data = data.iloc[-1]
signal = "HOLD"

if significant_news:
    print("Significant positive news detected. Consider buying.")
else:
    if (latest_data['Close'] > latest_data['50_MA'] and
        latest_data['Close'] > latest_data['200_MA'] and
        latest_data['RSI'] < RSI_OVERSOLD):
        signal = "BUY"
    elif (latest_data['Close'] < latest_data['50_MA'] and
          latest_data['Close'] < latest_data['200_MA'] and
          latest_data['RSI'] > RSI_OVERBOUGHT):
        signal = "SELL"

print(f"Trading Signal for AAPL: {signal}")

# Note: The actual buying, selling, and other trading operations are not included in this script.
# You'd need to integrate with a brokerage API to execute trades.
