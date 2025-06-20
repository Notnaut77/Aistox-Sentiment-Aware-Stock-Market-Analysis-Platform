import tweepy
import json
import os
from datetime import datetime

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAMN22gEAAAAA9zsM9sW32ZWBE4hACyffOrrs9UE%3D5GFtTJyjiStkKexLPecyZ1PG2ikuXirGpLpyWVliksZXAjKoX5"
OUTPUT_FILE = "Data_collector/twitter/tweets_stream.json"

class TweetStreamer(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        tweet_data = {
            "id": tweet.id,
            "text": tweet.text,
            "created_at": datetime.now().isoformat()
        }
        print(f"[Tweet] {tweet.text}\n")
        with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(tweet_data, ensure_ascii=False) + "\n")

    def on_connection_error(self):
        print("[!] Connection error. Restarting stream...")
        self.disconnect()

def start_stream():
    streamer = TweetStreamer(BEARER_TOKEN)

    rules = streamer.get_rules().data
    if rules:
        rule_ids = [rule.id for rule in rules]
        streamer.delete_rules(rule_ids)

    streamer.add_rules(tweepy.StreamRule("$TCS OR $INFY OR #StockMarket OR #Nifty50"))
    streamer.filter(tweet_fields=["created_at", "lang"], expansions=[], threaded=True)

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    start_stream()
