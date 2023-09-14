from pydantic import BaseModel
from datetime import datetime

class SensorData(BaseModel):
    sensor_id : str 
    value : float
    timestamp : str

class SensorDataMongo(BaseModel):
    _id: str
    payload: SensorData

class ReadingInterval(BaseModel):
    start_time: datetime
    end_time: datetime
