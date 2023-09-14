import paho.mqtt.client as mqtt
import json
import time
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def publish_sensor_data():
    client = mqtt.Client("Publisher")
    client.connect("localhost", 1883)

    sensor_ids = ["sensor1", "sensor2", "sensor3"]
    
    while True:
        for sensor_id in sensor_ids:
            temperature_value = round(random.uniform(20.0, 30.0), 2)
            humidity_value = round(random.uniform(40.0, 60.0), 2)

            temperature_data = {
                "sensor_id": sensor_id,
                "value": temperature_value,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            humidity_data = {
                "sensor_id": sensor_id,
                "value": humidity_value,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            
            client.publish("sensors/temperature", json.dumps(temperature_data))
            client.publish("sensors/humidity", json.dumps(humidity_data))
            logger.info("Data published successfully...!")
            time.sleep(25)  # Sleep for 25 seconds