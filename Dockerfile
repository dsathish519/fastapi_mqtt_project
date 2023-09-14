# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set the working directory to /app
WORKDIR /usr/src/main

# Copy the current directory contents into the container at /app
COPY . /main

# Run package updates and install redis
RUN apt-get update \ 
    && apt-get install -y redis-server

# Run install mosquitto broker
RUN apt-get install -y mosquitto mosquitto-client

# Copy just the requirements.txt
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
