import pandas as pd
import os
import json
import time
from kafka import KafkaProducer

PROJECT_ROOT = "/home/latitude/internet-pulse-platform"

RAW_PATH = os.path.join(PROJECT_ROOT, "data_lake/raw_news_data.csv")

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

sent_titles = set()

print("Kafka Producer started...")

while True:

    if not os.path.exists(RAW_PATH):
        print("Raw CSV not found.")
        time.sleep(10)
        continue

    df = pd.read_csv(RAW_PATH)

    new_articles = df[~df["title"].isin(sent_titles)]

    if not new_articles.empty:

        for _, row in new_articles.iterrows():

            article = row.to_dict()

            producer.send("news_topic", article)

            sent_titles.add(article["title"])

            print("Sent:", article["title"])

        producer.flush()

    else:
        print("No new articles")

    time.sleep(10)