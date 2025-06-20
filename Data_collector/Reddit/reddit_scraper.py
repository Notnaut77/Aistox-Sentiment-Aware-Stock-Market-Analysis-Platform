import praw
import json
import os

REDDIT_CLIENT_ID = ""
REDDIT_SECRET = ""
REDDIT_USER_AGENT = ""

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "reddit_posts.json")
SUBREDDITS = ["IndiaInvestments", "StockMarket", "IndianStreetBets", "Nifty50", "IndianStockMarket"]
KEYWORDS = ["TCS", "INFY", "nifty", "market", "stock"]

def collect_posts(limit=100):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    posts = []

    for sub in SUBREDDITS:
        for submission in reddit.subreddit(sub).hot(limit=limit):
            text = f"{submission.title} {submission.selftext}"
            if any(keyword.lower() in text.lower() for keyword in KEYWORDS):
                posts.append({
                    "subreddit": sub,
                    "title": submission.title,
                    "text": submission.selftext,
                    "score": submission.score,
                    "url": submission.url,
                    "created_utc": submission.created_utc
                })

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

    print(f"[✓] Collected {len(posts)} posts from Reddit")

if __name__ == "__main__":
    collect_posts()
