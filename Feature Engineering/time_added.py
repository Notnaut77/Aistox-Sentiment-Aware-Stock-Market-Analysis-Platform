
import pandas as pd

df = pd.read_csv("combined_with_ticker_api.csv")

# Convert `published` to datetime format
df["published"] = pd.to_datetime(df["published"], errors="coerce")

# Extract date, hour, weekday
df["date"] = df["published"].dt.date
df["hour"] = df["published"].dt.hour
df["weekday"] = df["published"].dt.day_name()

# Save to new file
df.to_csv("combined_with_time_features.csv", index=False)
print("[✓] Time-based features added → combined_with_time_features.csv")
