# 🌐 Internet Pulse Platform

A real-time news analytics pipeline that ingests, processes, and visualizes live news data using modern data engineering tools.

---

## 🚀 Overview

Internet Pulse Platform is an end-to-end **real-time data engineering project** that demonstrates how streaming systems work in production.

It collects live news data from APIs, streams it through a distributed pipeline, processes it in real time, and displays insights on an interactive dashboard.

---

## 🧱 Architecture

```
News API → Airflow → Kafka → Spark → Streamlit Dashboard
                         ↓
                     Data Lake (Batch Storage)
```

---

## ⚙️ Tech Stack

* **Apache Kafka** – Real-time event streaming
* **Apache Spark** – Stream processing
* **Apache Airflow** – Workflow orchestration
* **Streamlit** – Dashboard & visualization
* **Python** – Core development

---

## ⚡ Key Features

* 🔴 Real-time news ingestion pipeline
* 📡 Kafka-based streaming architecture
* ⚙️ Spark transformations on streaming data
* 📊 Live dashboard with auto-refresh
* 🧠 Top authors analytics
* 📈 Hourly publishing trend visualization
* 🗂️ Data lake for batch storage

---

## 📊 Dashboard

### 📰 Latest News

* Displays latest 100 articles
* Auto-refresh every 5 seconds

### 📈 Metrics

* Top 10 authors (ranked by article count)
* Articles published per hour (time-series chart)

---

## 📁 Project Structure

```
internet-pulse-platform/
│
├── dags/                 # Airflow DAGs
├── dashboard/            # Streamlit app
├── data_ingestion/       # API ingestion scripts
├── data_lake/            # Raw & processed data
├── kafka/                # Producers & consumers
├── spark_processing/     # Spark jobs
├── scripts/              # Utilities
├── docs/                 # Documentation
│
├── requirements.txt
├── run_pipeline.sh
└── README.md
```

---

## ▶️ Getting Started

### 1️⃣ Clone Repository

```
git clone https://github.com/YOUR_USERNAME/internet-pulse-platform.git
cd internet-pulse-platform
```

### 2️⃣ Setup Environment

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3️⃣ Run Pipeline

```
./run_pipeline.sh
```

### 4️⃣ Launch Dashboard

```
streamlit run dashboard/app.py
```

---

## 🔄 Data Flow

1. Airflow fetches news data from API
2. Data is pushed to Kafka topics
3. Spark processes streaming data
4. Consumer writes data to JSON (data lake)
5. Streamlit reads and visualizes data in real-time

---

## 🎯 Use Case

This project simulates a **real-time analytics platform** used in:

* News aggregation systems
* Social media analytics
* Monitoring & alerting platforms
* Data streaming pipelines

---

## 🚧 Future Improvements

* Dockerize entire pipeline
* Deploy on AWS (EC2 / MSK / S3)
* Add sentiment analysis (NLP)
* Real-time alerting system
* Replace JSON with scalable storage (Parquet / Delta Lake)

---

## 👨‍💻 Author

**Tejas Agrahari**

---

## ⭐ If you like this project

Give it a star ⭐ on GitHub!
