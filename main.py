from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from confluent_kafka import Producer
import json

app = FastAPI(title="Kafka Image Producer API")


# 1. Define the Expected Data Structure
class ImagePayload(BaseModel):
    filename: str
    base64_data: str


# 2. Configure the Kafka Producer
conf = {"bootstrap.servers": "localhost:9092", "message.max.bytes": 10485760}
producer = Producer(conf)
TOPIC_NAME = "image-processing-topic"


def delivery_report(err, msg):
    """Callback to confirm message delivery to Kafka"""
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to topic '{msg.topic()}'")


# 3. Create the POST Endpoint
@app.post("/upload-image/")
async def upload_image(payload: ImagePayload):
    try:
        # Create a dictionary payload
        kafka_message = {"filename": payload.filename, "data": payload.base64_data}

        # Convert the dictionary to a JSON string and encode to bytes
        json_bytes = json.dumps(kafka_message).encode("utf-8")

        # Send to Kafka
        producer.produce(TOPIC_NAME, value=json_bytes, callback=delivery_report)

        # Trigger any available delivery report callbacks
        producer.flush()

        return {
            "status": "success",
            "message": f"Image '{payload.filename}' has been safely stored in Kafka.",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
