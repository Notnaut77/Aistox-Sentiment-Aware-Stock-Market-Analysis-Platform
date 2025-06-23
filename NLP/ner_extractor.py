import spacy
import json
import os

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    return [
        {"text": ent.text, "label": ent.label_}
        for ent in doc.ents
        if ent.label_ in ["ORG", "GPE", "PRODUCT", "PERSON"]
    ]

def process_ner(input_path, output_path, text_field="cleaned_text"):
    with open(input_path, "r", encoding="utf-8") as infile:
        data = json.load(infile)

    output_data = []
    for entry in data:
        output_data.append({
            "entities": extract_entities(entry.get(text_field, "")),
            "published": entry.get("published", ""),
            "source": entry.get("source", "")
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as outfile:
        json.dump(output_data, outfile, indent=4, ensure_ascii=False)

    print(f"[✓] NER processed and saved → {output_path}")

sources = [
    {
        "input": "Data_collector/reddit/reddit_posts_cleaned.json",
        "output": "Data_collector/reddit/reddit_posts_ner.json"
    },
    {
        "input": "Data_collector/News/news_articles_cleaned.json",
        "output": "Data_collector/News/news_articles_ner.json"
    }
]

for src in sources:
    process_ner(src["input"], src["output"])
