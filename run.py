import subprocess
import sys
import time
from confluent_kafka.admin import AdminClient, NewTopic


def setup_kafka_topics():
    print("-> Running pre-flight checks...")
    # Connect to the Kafka broker as an Admin
    admin_client = AdminClient({"bootstrap.servers": "localhost:9092"})

    # Define the topic we need
    topic_name = "image-processing-topic"
    new_topic = NewTopic(topic_name, num_partitions=1, replication_factor=1)

    # Attempt to create the topic
    fs = admin_client.create_topics([new_topic])

    for topic, future in fs.items():
        try:
            future.result()  # This will complete if creation is successful
            print(f"   ✅ Created missing topic: '{topic}'")
        except Exception as e:
            # If the topic already exists, it throws an error we can safely ignore
            print(f"   ✅ Topic '{topic}' is ready.")


def start_services():
    print("🚀 Starting Kafka Pipeline...")

    # 1. Ensure topics exist BEFORE starting services
    setup_kafka_topics()

    # 2. Start the Consumer in the background
    print("-> Starting Consumer...")
    consumer_process = subprocess.Popen([sys.executable, "consumer.py"])

    # 3. Start the FastAPI server (Producer)
    print("-> Starting FastAPI (Producer)...")
    fastapi_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"]
    )

    try:
        # Keep the main script running to listen for Ctrl+C
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down processes...")
        fastapi_process.terminate()
        consumer_process.terminate()
        fastapi_process.wait()
        consumer_process.wait()
        print("✅ Shutdown complete.")


if __name__ == "__main__":
    start_services()
