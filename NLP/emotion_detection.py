import json
import os
from nrclex import NRCLex
from collections import Counter

def detect_emotions(text):
    if not text:
        return []
    emotion = NRCLex(text)
    emotion_counter = Counter(emotion.raw_emotion_scores)
    top_emotions = [e for e, count in emotion_counter.most_common(3)]
    return top_emotions

def process_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    output_data = []
    for entry in data:
        cleaned = entry.get("cleaned_text", "")
        output_data.append({
            "emotion": detect_emotions(cleaned),
            "published": entry.get("published", ""),
            "source": entry.get("source", "")
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(output_data, outfile, indent=4, ensure_ascii=False)

    print(f"[✓] Emotions saved to → {output_path}")

sources = [
    {
        "input": "Data_collector/News/news_articles_cleaned.json",
        "output": "Data_collector/News/news_articles_emotions.json"
    },
    {
        "input": "Data_collector/reddit/reddit_posts_cleaned.json",
        "output": "Data_collector/reddit/reddit_posts_emotions.json"
    }
]

for src in sources:
    process_file(src["input"], src["output"])
