from motor.motor_asyncio import AsyncIOMotorClient
import paho.mqtt.client as mqtt
from .my_redis import get_redis_client
from fastapi import Depends
import json
import asyncio
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
stop_thread = False

r = get_redis_client()

# Store data in MongoDB asynchronously
async def store_in_mongodb(payload, topic, mongodb_client):
    try:
        database_name = "sensor_data"
        collection_name = topic.split("/")[-1]  # Extracting the 'humidity' or 'temperature' part
        collection = mongodb_client[database_name][collection_name]
        document = {"payload": payload}
        await collection.insert_one(document)
        logger.info(f"Stored in MongoDB: {document}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


# MQTT Subscription Callback
def on_message(client, userdata, message):
    global stop_thread
    payload = json.loads(message.payload.decode())
    topic = message.topic

    sensor_id = payload['sensor_id']  # Extracting the sensor_id part

    redis_key = f"{sensor_id}_{topic.split('/')[-1]}"  # create a unique Redis key
    r.lpush(redis_key, json.dumps(payload)) 
    r.ltrim(redis_key, 0, 9)  # only keep the latest 10 elements

    logger.info(f"redis: {r.lrange(redis_key, 0, 9)}")
    
    logger.info(f"Received message on topic '{message.topic}': {payload}")

    loop, mongodb_client = userdata

    if loop.is_closed():
        logger.info("Event loop closed. Exiting thread.")
        stop_thread = True  # Signal to stop the thread
        return
    future = asyncio.run_coroutine_threadsafe(
        store_in_mongodb(payload, topic, mongodb_client), loop
    )
    future.result()


def subscribe_mqtt(loop, mongodb_client):
    global stop_thread
    userdata = (loop, mongodb_client)
    client = mqtt.Client(userdata = userdata)
    try:
        client.connect("localhost", 1883)
    except Exception as e:
        logger.error(f"Could not connect to MQTT broker: {e}")
        return
    client.subscribe("sensors/#")
    client.on_message = on_message
    while not stop_thread:  # Keep running until signaled to stop
        client.loop(25)
    client.disconnect()


