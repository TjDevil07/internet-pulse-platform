import json
import os
from kafka import KafkaConsumer

LATEST_FILE = "data_lake/latest_news.json"

# Ensure folder exists
os.makedirs("data_lake", exist_ok=True)

consumer = KafkaConsumer(
    "news_topic",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

print("Dashboard consumer started...")

buffer = []

# Load existing buffer if file exists
if os.path.exists(LATEST_FILE):
    try:
        with open(LATEST_FILE, "r") as f:
            buffer = json.load(f)
    except:
        buffer = []

for message in consumer:
    article = message.value

    buffer.append(article)

    # Keep only latest 100
    if len(buffer) > 100:
        buffer.pop(0)

    with open(LATEST_FILE, "w") as f:
        json.dump(buffer, f, indent=2)

    print("Dashboard updated:", article.get("title", "No Title"))