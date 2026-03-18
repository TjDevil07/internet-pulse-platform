import requests
import pandas as pd
import os
from datetime import datetime

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
API_KEY = "T-hY8zZPqfyLYjx4fJsy6wKHSKO86t2QSQ9aPG-fBHIab6at"
API_URL = "https://api.currentsapi.services/v1/latest-news"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_NEWS_PATH = os.path.join(BASE_DIR, "../data_lake/raw_news_data.csv")

BUFFER_SIZE = 100
REQUEST_TIMEOUT = 10

# Ensure data_lake folder exists
os.makedirs(os.path.dirname(RAW_NEWS_PATH), exist_ok=True)

# ---------------------------------------------------
# Fetch News from API
# ---------------------------------------------------
params = {
    "apiKey": API_KEY,
    "language": "en",
    "category": "general"
}

print("Fetching latest news from API...")

try:
    response = requests.get(API_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
except Exception as e:
    print(f"API Connection Error: {e}")
    exit()

news_data = response.json().get("news", [])

if not news_data:
    print("No news returned by API.")
    exit()

# ---------------------------------------------------
# Normalize API Data
# ---------------------------------------------------
articles = []

for article in news_data:

    articles.append({
        "title": article.get("title", "").strip(),
        "description": article.get("description", "").strip(),
        "author": article.get("author", "Unknown"),
        "published": article.get("published", ""),
        "fetched_at": datetime.utcnow().isoformat()
    })

new_df = pd.DataFrame(articles)

# Convert datetime
new_df["published"] = pd.to_datetime(new_df["published"], errors="coerce")

# ---------------------------------------------------
# Load Existing Data
# ---------------------------------------------------
if os.path.exists(RAW_NEWS_PATH) and os.path.getsize(RAW_NEWS_PATH) > 0:

    try:
        existing_df = pd.read_csv(RAW_NEWS_PATH)
        existing_df["published"] = pd.to_datetime(existing_df["published"], errors="coerce")

        print(f"Loaded existing dataset with {len(existing_df)} records.")

    except Exception as e:
        print(f"Error reading existing CSV: {e}")
        existing_df = pd.DataFrame()

    combined_df = pd.concat([new_df, existing_df], ignore_index=True)

    # Remove duplicate articles
    combined_df = combined_df.drop_duplicates(subset=["title"], keep="first")

else:

    print("No existing CSV found. Creating new dataset.")
    combined_df = new_df

# ---------------------------------------------------
# Maintain Rolling Buffer
# ---------------------------------------------------
combined_df = combined_df.sort_values(by="published", ascending=False)

final_df = combined_df.head(BUFFER_SIZE)

# ---------------------------------------------------
# Save Updated CSV
# ---------------------------------------------------
try:
    final_df.to_csv(RAW_NEWS_PATH, index=False)
except Exception as e:
    print(f"Error saving CSV: {e}")
    exit()

# ---------------------------------------------------
# Summary Output
# ---------------------------------------------------
print("\n--- News Collection Summary ---")
print(f"Articles fetched from API: {len(new_df)}")
print(f"Articles stored in rolling buffer: {len(final_df)}")
print(f"Buffer limit: {BUFFER_SIZE}")
print(f"Saved file: {RAW_NEWS_PATH}")
print("Collection completed successfully.\n")
