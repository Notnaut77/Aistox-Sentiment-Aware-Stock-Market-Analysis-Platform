import json
import re
import nltk
import spacy
import emoji
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
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

def process_file(input_path, output_path, text_fields):
    with open(input_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    for entry in data:
        combined_text = " ".join([entry.get(field, "") for field in text_fields])
        entry["cleaned_text"] = preprocess_text(combined_text)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)
    print(f"[✓] Cleaned and saved → {output_path}")

sources = [
    {
        "input": "Data_collector/News/news_articles.json",
        "output": "Data_collector/News/news_articles_cleaned.json",
        "fields": ["title", "content"]
    },
    {
        "input": "Data_collector/Reddit/reddit_posts.json",
        "output": "Data_collector/Reddit/reddit_posts_cleaned.json",
        "fields": ["title", "text"]
    }
]

for src in sources:
    process_file(src["input"], src["output"], src["fields"])
