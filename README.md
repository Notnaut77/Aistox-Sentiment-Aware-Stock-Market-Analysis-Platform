# Aistox: Sentiment-Aware Stock Market Direction Classifier

**Aistox** is a full-stack NLP pipeline designed to classify the **direction** of stock price movement (up or down) based on textual signals extracted from financial news, Reddit posts, and optionally Twitter.

> This is not about building a market oracle. It’s about extracting structure from noise, exploring sentiment-driven narratives, and creating transparent, interpretable prediction systems.

---

## Problem Statement

Can the language surrounding financial markets — headlines, posts, tweets — help signal the **next short-term direction** in stock prices?

We don’t predict exact prices. We classify **direction**, based on how markets tend to **react** to sentiment-heavy information.

---

## Core Features

- Scrape and preprocess financial text data
- Apply multi-layered NLP: sentiment, emotion detection, NER, and topic modeling
- Label samples based on historical stock movement
- Train machine learning models to classify direction
- Perform real-time inference on new, incoming data

---

## Pipeline Architecture

### 1. Data Collection

- Sources: News RSS feeds, Reddit (finance subreddits), optional Twitter
- Stored Fields: title, content, timestamp, source URL

### 2. Textual Feature Engineering

- **Cleaning**: lowercasing, stopword removal, lemmatization (via spaCy)
- **Sentiment Analysis**: VADER and TextBlob
- **Emotion Tags**: NRC Emotion Lexicon via NRCLex
- **Named Entity Recognition**: spaCy (`ORG`, `GPE`, `PRODUCT`, `PERSON`)
- **Topic Modeling**: BERTopic with transformer embeddings
- **Temporal Features**: hour of day, day of week, etc.

### 3. Labeling with Price Movement

- Extract named entities and map to stock tickers (Yahoo Finance API)
- Fetch historical prices at time `t` and `t+1` day
- Label: `1` if `close(t+1) > close(t)` else `0`

### 4. Model Training

- Vectorization: TF-IDF on preprocessed text
- Combine with numerical features: sentiment scores, emotion tags, topic ID
- Model: Baseline with Logistic Regression
- Save trained model and vectorizer for inference

---

## Setup

```bash
# Clone repository
git clone https://github.com/your-username/aistox.git
cd aistox

# Install dependencies
pip install -r requirements.txt

# Run modules
python Data_collector/news_scraper.py
python Feature_Engineering/preprocess.py
python Feature_Engineering/sentiment.py
# ...
python Model_Training/train_model.py
```

---

## References

### Research Papers

- Tetlock et al., *Financial News and Stock Returns*, AER  
- Google Research, *Event Extraction for Financial Forecasting*, arXiv:2006.11339  
- Bing Liu, *Sentiment Analysis and Opinion Mining*  
- M. L. de Prado, *Advances in Financial Machine Learning*

### Libraries and Tools

- spaCy  
- VADER  
- TextBlob  
- NRCLex  
- BERTopic  
- Yahoo Finance API

### Related GitHub Projects

- [Stocksight](https://github.com/shawnsr/Stocksight)  
- [FinBERT](https://github.com/ProsusAI/finBERT)  
- [News Sentiment Stock Price](https://github.com/MaartenGr/BERTopic)

### Lectures & Tutorials

- Stanford CS224n: NLP with Deep Learning  
- Georgia Tech: ML for Trading (Udacity)  
- BERTopic Tutorial by Maarten Grootendorst

---

## Disclaimer

This project is intended for educational and experimental purposes only. Stock markets are complex and influenced by many factors beyond language. This tool does not provide financial advice or guarantee predictive accuracy.

---

## Future Directions

- Replace TF-IDF with FinBERT embeddings
- Incorporate XGBoost and ensemble models
- Backtesting with P&L simulation
- Build a live dashboard for predictions
- Deploy inference API using FastAPI

---

## License

This project is released under the MIT License. Feel free to use, modify, and build upon it.
