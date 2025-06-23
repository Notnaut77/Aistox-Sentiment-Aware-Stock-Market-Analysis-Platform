import json, os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

analyzer = SentimentIntensityAnalyzer()

def label_from_compound(score, pos=0.05, neg=-0.05):
    if score >= pos:
        return "POS"
    elif score <= neg:
        return "NEG"
    else:
        return "NEU"

def classify_file(input_path, output_path, text_field="cleaned_text"):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = []
    for entry in data:
        text = entry.get(text_field, "")
        vs = analyzer.polarity_scores(text)
        tb = TextBlob(text).sentiment.polarity

        result.append({
            "sentiment": {
                "vader_compound": vs["compound"],
                "vader_pos": vs["pos"],
                "vader_neu": vs["neu"],
                "vader_neg": vs["neg"],
                "vader_label": label_from_compound(vs["compound"]),
                "textblob_polarity": tb,
                "textblob_label": label_from_compound(tb)
            },
            "published": entry.get("published", ""),
            "source": entry.get("source", "")
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"[✓] Classified → {output_path}")

sources = [
    {
        "input": "Data_collector/News/news_articles_cleaned.json",
        "output": "Data_collector/News/news_articles_scored.json"
    },
    {
        "input": "Data_collector/twitter/tweets_stream_cleaned.json",
        "output": "Data_collector/twitter/tweets_stream_scored.json"
    },
    {
        "input": "Data_collector/Reddit/reddit_posts_cleaned.json",
        "output": "Data_collector/Reddit/reddit_posts_scored.json"
    }
]

for s in sources:
    classify_file(s["input"], s["output"])
