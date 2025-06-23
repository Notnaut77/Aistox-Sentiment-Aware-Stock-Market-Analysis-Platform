import pandas as pd
import ast

df = pd.read_csv("combined_with_time_features.csv")

# Parse stringified dict if necessary
def parse_sentiment(x):
    try:
        return ast.literal_eval(x) if isinstance(x, str) else x
    except:
        return {}

sentiment_df = df["sentiment"].apply(parse_sentiment).apply(pd.Series)

# Rename columns for clarity
sentiment_df = sentiment_df.rename(columns={
    "vader_compound": "sent_vader_compound",
    "vader_label": "sent_vader_label",
    "vader_pos": "sent_vader_pos",
    "vader_neu": "sent_vader_neu",
    "vader_neg": "sent_vader_neg",
    "textblob_polarity": "sent_textblob_polarity",
    "textblob_label": "sent_textblob_label"
})

# Merge with main DataFrame
df = pd.concat([df, sentiment_df], axis=1)

# Drop original sentiment column if desired
df = df.drop(columns=["sentiment"])

# Save to new file
df.to_csv("combined_with_sentiment_flat.csv", index=False)
print("[✓] Sentiment features flattened → combined_with_sentiment_flat.csv")
