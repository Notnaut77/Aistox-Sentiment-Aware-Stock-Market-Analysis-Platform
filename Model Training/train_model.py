import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from scipy.sparse import hstack
import joblib
import os

df = pd.read_csv("../Feature_Engineering/final_labeled_data.csv")

df = df.dropna(subset=["cleaned_text", "label"])
df["label"] = df["label"].astype(int)

text_data = df["cleaned_text"]
y = df["label"]

vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X_text = vectorizer.fit_transform(text_data)

numeric_features = [
    "sent_vader_compound", "sent_textblob_polarity", "topic_id", "hour"
] + [col for col in df.columns if col.startswith("emotion_")]

X_numeric = df[numeric_features].fillna(0)

X_all = hstack([X_text, X_numeric])

X_train, X_test, y_train, y_test = train_test_split(X_all, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

os.makedirs("models", exist_ok=True)
os.makedirs("vectorizers", exist_ok=True)

joblib.dump(model, "models/logistic_model_full.pkl")
joblib.dump(vectorizer, "vectorizers/tfidf_vectorizer_full.pkl")

print("[✓] Full model with engineered features saved.")
