import feedparser
from newspaper import Article
import json
from datetime import datetime
import os

RSS_FEEDS = [
    "https://economictimes.indiatimes.com/rss/markets/rssfeeds/1977021501.cms",
    "https://www.livemint.com/rss/market",
    "https://www.reuters.com/finance/markets/rss"
]

def fetch_news_articles():
    articles = []
    for feed_url in RSS_FEEDS:
        print(f"\n[+] Parsing feed: {feed_url}")
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            try:
                article = Article(entry.link)
                article.download()
                article.parse()
                article_data = {
                    "title": article.title,
                    "url": entry.link,
                    "published": entry.published if 'published' in entry else None,
                    "source": feed_url,
                    "content": article.text,
                    "scraped_at": datetime.now().isoformat()
                }
                articles.append(article_data)
            except Exception as e:
                print(f"[!] Failed to parse article: {entry.link}\n    Reason: {e}")
                continue
    return articles

def save_articles_to_json(articles, file_path="news_articles.json"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)
    print(f"\n[✓] Saved {len(articles)} articles to {file_path}")

if __name__ == "__main__":
    news_articles = fetch_news_articles()
    save_articles_to_json(news_articles, "Data_collector/News/news_articles.json")
