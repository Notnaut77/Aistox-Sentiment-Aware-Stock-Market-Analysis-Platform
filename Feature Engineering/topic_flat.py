import pandas as pd
import ast

df = pd.read_csv("combined_with_emotions_flat.csv")

def parse_keywords(val):
    try:
        parsed = ast.literal_eval(val) if isinstance(val, str) else val
        return ", ".join(parsed) if isinstance(parsed, list) else str(parsed)
    except:
        return ""

df["topic_keywords"] = df["topic_keywords"].apply(parse_keywords)
df["topic_id"] = pd.to_numeric(df["topic_id"], errors="coerce")

df.to_csv("combined_with_topics_flat.csv", index=False)
print("[✓] Topic fields flattened → combined_with_topics_flat.csv")
