import pandas as pd
import ast

df = pd.read_csv("combined_with_sentiment_flat.csv")

emotion_tags = ["fear", "anger", "anticipation", "trust", "surprise", "sadness", "joy", "disgust"]

def parse_emotions(emotion_list):
    try:
        parsed = ast.literal_eval(emotion_list) if isinstance(emotion_list, str) else emotion_list
        return {f"emotion_{e}": int(e in parsed) for e in emotion_tags}
    except:
        return {f"emotion_{e}": 0 for e in emotion_tags}

emotion_df = df["emotion"].apply(parse_emotions).apply(pd.Series)

df = pd.concat([df, emotion_df], axis=1)
df = df.drop(columns=["emotion"])

df.to_csv("combined_with_emotions_flat.csv", index=False)
print("[✓] Emotion tags flattened → combined_with_emotions_flat.csv")
