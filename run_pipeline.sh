#!/bin/bash

echo "========================================="
echo "Starting Internet Pulse Platform Pipeline"
echo "========================================="

BASE_DIR=~/internet-pulse-platform
KAFKA_DIR=~/kafka_setup

echo ""
echo "Setting environment"
source venv/bin/activate

echo ""
echo "Stopping old services..."

pkill -9 -f kafka
pkill -9 -f zookeeper
pkill -9 -f spark
pkill -9 -f streamlit
pkill -9 -f airflow
pkill -9 -f producer
pkill -9 -f consumer

# CLEANUP: Remove stale Airflow scheduler lock to prevent start failures
rm -f ~/airflow/airflow-scheduler.pid

sleep 3

echo ""
echo "Cleaning Kafka state..."

rm -rf /tmp/kafka-logs
rm -rf /tmp/zookeeper
rm -rf $KAFKA_DIR/kafka-logs

sleep 2

echo ""
echo "Starting Zookeeper..."

cd $KAFKA_DIR
nohup bin/zookeeper-server-start.sh config/zookeeper.properties > zookeeper.log 2>&1 &

sleep 5

echo ""
echo "Starting Kafka Broker..."

nohup bin/kafka-server-start.sh config/server.properties > kafka.log 2>&1 &

echo ""
echo "Waiting for Kafka broker..."

for i in {1..20}
do
    nc -z localhost 9092
    if [ $? -eq 0 ]; then
        echo "Kafka is ready!"
        break
    fi
    echo "Waiting..."
    sleep 2
done

echo ""
echo "Creating Kafka topic..."

bin/kafka-topics.sh --create \
--topic news_topic \
--bootstrap-server localhost:9092 \
--replication-factor 1 \
--partitions 1 \
--if-not-exists

sleep 2

echo ""
echo "Starting Kafka Producer..."

cd $BASE_DIR/kafka
python3 producer.py &

sleep 2

echo ""
echo "Starting Spark Consumer..."

cd $BASE_DIR/kafka
python3 consumer_spark.py &

sleep 2

echo ""
echo "Starting Dashboard Consumer..."

cd $BASE_DIR/kafka
python3 consumer_streamlit.py &

sleep 2

echo ""
echo "Starting Airflow 3 Components..."

# 1. Initialize/Migrate the database
airflow db migrate

# 2. Start the API Server (Powers the UI)
nohup airflow api-server --port 8080 > airflow_api.log 2>&1 &

# 3. Start the Scheduler
nohup airflow scheduler > airflow_scheduler.log 2>&1 &

# 4. Start the DAG Processor (Mandatory to parse the new Hourly schedule)
nohup airflow dag-processor > airflow_dag_processor.log 2>&1 &

# 5. Ensure the DAG is turned on (unpaused)
sleep 5
airflow dags unpause news_pipeline

sleep 5

echo ""
echo "Starting Streamlit Dashboard..."

cd $BASE_DIR/dashboard
nohup streamlit run app.py &

sleep 3

echo ""
echo "========================================="
echo "PIPELINE STARTUP REPORT (HOURLY)"
echo "========================================="

# Status Check Functions
check_port() {
    nc -z localhost $1 && echo "✅ $2: Running (Port $1)" || echo "❌ $2: Down"
}

check_proc() {
    pgrep -f "$1" > /dev/null && echo "✅ $2: Running" || echo "❌ $2: Down"
}

check_proc "kafka" "Kafka Broker"
check_port 8080 "Airflow API/UI"
check_proc "airflow scheduler" "Airflow Scheduler"
check_proc "airflow dag-processor" "Airflow DAG Processor"
check_port 8501 "Streamlit Dashboard"

echo ""
echo "Access services:"
echo "Airflow UI: http://localhost:8080"
echo "Streamlit Dashboard: http://localhost:8501"
echo "========================================="