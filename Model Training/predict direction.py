import json
import pandas as pd
import joblib
import re
import emoji
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nrclex import NRCLex
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from scipy.sparse import hstack
from datetime import datetime

import nltk
nltk.download("punkt")
nltk.download("stopwords")

stop_words = set(stopwords.words("english"))
nlp = spacy.load("en_core_web_sm")
analyzer = SentimentIntensityAnalyzer()

emotion_tags = ["fear", "anger", "anticipation", "trust", "surprise", "sadness", "joy", "disgust"]

vectorizer = joblib.load("vectorizers/tfidf_vectorizer_full.pkl")
model = joblib.load("models/logistic_model_full.pkl")

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)
    text = re.sub(r"\@\w+|\#", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    text = emoji.replace_emoji(text, replace="")
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    doc = nlp(" ".join(tokens))
    lemmas = [token.lemma_ for token in doc]
    return " ".join(lemmas)

def detect_emotions(text):
    emotion = NRCLex(text)
    return {f"emotion_{e}": int(e in emotion.raw_emotion_scores) for e in emotion_tags}

def extract_sentiment(text):
    vs = analyzer.polarity_scores(text)
    tb = TextBlob(text).sentiment.polarity
    return {
        "sent_vader_compound": vs["compound"],
        "sent_textblob_polarity": tb,
        "hour": datetime.now().hour,
        "topic_id": 0  
    }

def predict_direction(raw_text):
    cleaned_text = preprocess_text(raw_text)
    X_text = vectorizer.transform([cleaned_text])
    emotion_feats = detect_emotions(cleaned_text)
    sentiment_feats = extract_sentiment(cleaned_text)
    all_feats = {**emotion_feats, **sentiment_feats}
    df_extra = pd.DataFrame([all_feats])
    X_final = hstack([X_text, df_extra])
    label = model.predict(X_final)[0]
    prob = model.predict_proba(X_final)[0][label]
    return label, prob

# EXAMPLE
if __name__ == "__main__":
    sample_text = """Fed raises interest rates again amid inflation concerns. Investors remain cautious."""
    label, confidence = predict_direction(sample_text)
    print(f"Prediction: {'UP 📈' if label == 1 else 'DOWN 📉'} with confidence {confidence:.2f}")
