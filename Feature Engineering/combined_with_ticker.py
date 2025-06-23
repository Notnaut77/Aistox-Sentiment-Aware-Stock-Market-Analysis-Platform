import pandas as pd
import ast
import requests
import time

df = pd.read_csv("merged.csv")

entity_to_ticker_cache = {}

def query_yahoo_ticker(entity_name):
    if entity_name in entity_to_ticker_cache:
        return entity_to_ticker_cache[entity_name]

    url = f"https://query1.finance.yahoo.com/v1/finance/search?q={entity_name}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("quotes", []):
                if item.get("quoteType") == "EQUITY":
                    ticker = item.get("symbol")
                    entity_to_ticker_cache[entity_name] = ticker
                    time.sleep(0.5)  # To respect rate limits
                    return ticker
    except Exception as e:
        print(f"[!] Error querying {entity_name}: {e}")

    entity_to_ticker_cache[entity_name] = None
    return None

def extract_first_org_ticker(entities):
    try:
        ents = ast.literal_eval(entities)
        for ent in ents:
            if isinstance(ent, dict) and ent.get("label") == "ORG":
                name = ent.get("text", "").strip()
                if name:
                    ticker = query_yahoo_ticker(name)
                    if ticker:
                        return ticker
    except Exception as e:
        print(f"[!] Failed to parse entities: {e}")
    return None

df["ticker"] = df["entities"].apply(extract_first_org_ticker)

df.to_csv("combined_with_ticker_api.csv", index=False)
print("[✓] Ticker column added using Yahoo Finance API → combined_with_ticker.csv")
