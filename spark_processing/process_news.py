import pandas as pd
import os

PROJECT_ROOT = "/home/latitude/internet-pulse-platform"

RAW_PATH = os.path.join(PROJECT_ROOT, "data_lake/raw_news_data.csv")
PROCESSED_PATH = os.path.join(PROJECT_ROOT, "data_lake/processed_news.csv")

if not os.path.exists(RAW_PATH):
    print("Raw data not found")
    exit()

df = pd.read_csv(RAW_PATH)

df["author"] = (
    df["author"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.title()
)

authors_df = df["author"].value_counts().reset_index()
authors_df.columns = ["top_authors", "count"]

df["published"] = pd.to_datetime(df["published"], errors="coerce")

df["hour"] = df["published"].dt.floor("h")

hour_df = df.groupby("hour").size().reset_index(name="article_count")

with open(PROCESSED_PATH, "w") as f:

    authors_df.to_csv(f, index=False)

    f.write("\n")

    hour_df.to_csv(f, index=False)

print("Processed metrics updated")