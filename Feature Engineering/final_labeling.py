import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

df = pd.read_csv("combined_with_topics_flat.csv")

df["date"] = pd.to_datetime(df["date"])
df = df.dropna(subset=["ticker", "date"])
df["ticker"] = df["ticker"].astype(str)

unique_tickers = df["ticker"].unique()
price_cache = {}

for ticker in unique_tickers:
    try:
        start = df[df["ticker"] == ticker]["date"].min() - timedelta(days=1)
        end = df[df["ticker"] == ticker]["date"].max() + timedelta(days=3)
        data = yf.download(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
        price_cache[ticker] = data["Close"]
    except Exception as e:
        print(f"[!] Error fetching {ticker}: {e}")

def get_label(row):
    ticker = row["ticker"]
    date = row["date"]
    try:
        today_price = price_cache[ticker].get(date)
        next_day = date + timedelta(days=1)
        while next_day not in price_cache[ticker].index and (next_day - date).days <= 3:
            next_day += timedelta(days=1)
        future_price = price_cache[ticker].get(next_day)
        if pd.notna(today_price) and pd.notna(future_price):
            return int(future_price > today_price)
    except:
        return None
    return None

df["label"] = df.apply(get_label, axis=1)

df.to_csv("final_labeled_data.csv", index=False)
print("[✓] Labeling complete → final_labeled_data.csv")
