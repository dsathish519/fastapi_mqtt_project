from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from routes import sensor  
from mongodb import get_mongo_db_client 
from routes.mqtt_publisher import publish_sensor_data 
from routes.mqtt_subscriber import subscribe_mqtt, stop_thread
import threading
import asyncio
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Sensor Data API")

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = await get_mongo_db_client()
    loop = asyncio.get_running_loop()
    threading.Thread(target=publish_sensor_data).start()
    threading.Thread(target=subscribe_mqtt, args=(loop, app.mongodb_client)).start()

# Closing connection
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
    global stop_thread
    stop_thread = True

app.include_router(sensor.router)

@app.get("/")
def root():
    return {"message": "HomePage"}