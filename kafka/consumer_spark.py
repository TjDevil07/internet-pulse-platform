import json
import subprocess
from kafka import KafkaConsumer
import os

PROJECT_ROOT = "/home/latitude/internet-pulse-platform"

PROCESS_SCRIPT = os.path.join(
    PROJECT_ROOT,
    "spark_processing/process_news.py"
)

consumer = KafkaConsumer(
    "news_topic",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="spark-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Spark consumer started...")

for message in consumer:

    article = message.value

    print("Processing:", article.get("title"))

    subprocess.run(["python3", PROCESS_SCRIPT])