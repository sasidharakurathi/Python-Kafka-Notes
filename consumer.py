from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import base64
import os

# 1. Setup an output directory for the images
OUTPUT_DIR = "saved_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Configure the Kafka Consumer
conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "image-saver-group",
    "auto.offset.reset": "earliest",
    "fetch.message.max.bytes": 10485760,
}

consumer = Consumer(conf)
TOPIC_NAME = "image-processing-topic"
consumer.subscribe([TOPIC_NAME])

print(f"Listening for images on '{TOPIC_NAME}'... Saving to ./{OUTPUT_DIR}/")

try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Consumer error: {msg.error()}")
                break

        # 3. Process the Message
        try:
            # Decode the raw Kafka bytes into a string, then parse the JSON
            message_str = msg.value().decode("utf-8")
            payload = json.loads(message_str)

            filename = payload.get("filename", "unnamed_image.png")
            base64_string = payload.get("data", "")

            # Strip out the metadata header if it exists (e.g., "data:image/png;base64,")
            if "," in base64_string:
                base64_string = base64_string.split(",")[1]

            # Decode the base64 string back into raw image bytes
            image_bytes = base64.b64decode(base64_string)

            # 4. Save the File
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(image_bytes)

            print(f"Success! Saved: {filepath}")

        except Exception as e:
            print(f"Failed to process image payload: {e}")

except KeyboardInterrupt:
    print("Shutting down consumer...")
finally:
    consumer.close()
