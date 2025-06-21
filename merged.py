import json
import os
import pandas as pd

sources = {
    "reddit": "Data_collector/reddit",
    "news": "Data_collector/News"
}

files = {
    "cleaned": "cleaned",
    "sentiment": "sentiment",
    "emotions": "emotions",
    "ner": "ner",
    "topics": "topics_bertopic"
}

for source, base_path in sources.items():
    datasets = {}
    for key, name in files.items():
        file_path = os.path.join(base_path, f"{source}_posts_{name}.json") if source == "reddit" else os.path.join(base_path, f"news_articles_{name}.json")
        with open(file_path, "r", encoding="utf-8") as f:
            datasets[key] = json.load(f)

    merged = []
    for i in range(len(datasets["cleaned"])):
        merged_entry = {}
        merged_entry["cleaned_text"] = datasets["cleaned"][i].get("cleaned_text", "")
        merged_entry.update({
            "sentiment": datasets["sentiment"][i].get("sentiment", datasets["sentiment"][i]),
            "emotion": datasets["emotions"][i].get("emotion", datasets["emotions"][i]),
            "entities": datasets["ner"][i].get("entities", []),
            "topic_id": datasets["topics"][i].get("topic_id", None),
            "topic_keywords": datasets["topics"][i].get("topic_keywords", [])
        })
        merged_entry["source"] = source
        merged.append(merged_entry)

    json_output_path = os.path.join(base_path, f"{source}_posts_final.json") if source == "reddit" else os.path.join(base_path, f"news_articles_final.json")
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=4, ensure_ascii=False)

    csv_output_path = json_output_path.replace(".json", ".csv")
    flat_data = []
    for entry in merged:
        flat_data.append({
            "cleaned_text": entry["cleaned_text"],
            "source": entry["source"],
            "sentiment": json.dumps(entry["sentiment"]),
            "emotion": json.dumps(entry["emotion"]),
            "entities": json.dumps(entry["entities"]),
            "topic_id": entry["topic_id"],
            "topic_keywords": ", ".join([kw[0] if isinstance(kw, list) else kw for kw in entry["topic_keywords"]])
        })
    df = pd.DataFrame(flat_data)
    df.to_csv(csv_output_path, index=False, encoding="utf-8")

    print(f"[✓] merged JSON → {json_output_path}")
    print(f"[✓]  merged CSV → {csv_output_path}")
