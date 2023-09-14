from fastapi import APIRouter, Depends, HTTPException, Body
from motor.motor_asyncio import AsyncIOMotorClient
from schemas import SensorDataMongo, ReadingInterval, SensorData
from mongodb import get_mongo_db_client
from .my_redis import get_redis_client
from typing import List
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=['Sensor_data'])

r = get_redis_client()

# fetch sensor data for the given date range
@router.get("/sensor_readings/{topic}", response_model=List[SensorDataMongo])
async def get_sensor_readings(topic: str,interval: ReadingInterval = Body(...),
                              mongo_client: AsyncIOMotorClient = Depends(get_mongo_db_client)):
    database_name = "sensor_data" 
    sensor_collection = mongo_client[database_name][topic]

    start_time_str = interval.start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time_str = interval.end_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Query MongoDB for readings within the specified time range
    query = {
            "payload.timestamp": {
               "$gte": str(start_time_str),
                "$lte": str(end_time_str)
            }
        }
    logger.info(f"query : {query}")
    readings = await sensor_collection.find(query).to_list(None)
    logger.info(f"readings: {readings}")
    if readings:
        return readings
    
    raise HTTPException(status_code=404, detail=f"No Data Found Under The Given Time Range")

# fetch last_ten_sensor reading
@router.get("/last_ten_readings", response_model=List[SensorData])
async def get_last_ten_readings(sensor_id: str, data_type: str):
    redis_key = f"{sensor_id}_{data_type}" 
    last_ten_readings = r.lrange(redis_key, 0, 9)  # get the last 10 readings
    logger.info(f"last_ten_readings: {last_ten_readings}")
    if last_ten_readings:
        return [json.loads(reading.decode()) for reading in last_ten_readings]
    else:
        raise HTTPException(status_code=404, detail=f"No readings found for sensor_id: {sensor_id}")
