import os
from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import datetime, timedelta
import uuid
import random
import time

# Define San Jose and San Francisco coordinates for simulation
SAN_JOSE_COORDINATES = {"latitude": 37.3382, "longitude": -121.8863}
SAN_FRANCISCO_COORDINATES = {"latitude": 37.7749, "longitude": -122.4194}

# Calculate the increments for movement simulation
LATITUDE_INCREMENT = (
    SAN_FRANCISCO_COORDINATES["latitude"] - SAN_JOSE_COORDINATES["latitude"]
) / 100
LONGITUDE_INCREMENT = (
    SAN_FRANCISCO_COORDINATES["longitude"] - SAN_JOSE_COORDINATES["longitude"]
) / 100

# Load environment variables for Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
VEHICLE_TOPIC = os.getenv("VEHICLE_TOPIC", "vehicle_data")
GPS_TOPIC = os.getenv("GPS_TOPIC", "gps_data")
TRAFFIC_TOPIC = os.getenv("TRAFFIC_TOPIC", "traffic_data")
WEATHER_TOPIC = os.getenv("WEATHER_TOPIC", "weather_data")
EMERGENCY_TOPIC = os.getenv("EMERGENCY_TOPIC", "emergency_data")

random.seed(42)  # Ensure reproducibility of random data
start_time = datetime.now()  # Initialize simulation start time
start_location = SAN_JOSE_COORDINATES.copy()  # Initialize starting location

def get_next_time():
    """Generate the next timestamp for data generation"""
    global start_time
    start_time += timedelta(seconds=random.randint(30, 60))
    return start_time

def generate_gps_data(device_id, timestamp, vehicle_type="private"):
    """Simulate GPS data for a vehicle"""
    return {
        "id": uuid.uuid4(),
        "device_id": device_id,
        "timestamp": timestamp,
        "speed": random.uniform(0, 40),  # km/h
        "direction": "North-East",
        "vehicle_type": vehicle_type,
    }

def generate_traffic_camera_data(device_id, timestamp, location, camera_id):
    """Simulate data from a traffic camera"""
    return {
        "id": uuid.uuid4(),
        "device_id": device_id,
        "timestamp": timestamp,
        "location": location,
        "camera_id": camera_id,
        "snapshot": "Base64EncodedString",  # Placeholder for image data
    }

def generate_weather_data(device_id, timestamp, location):
    """Simulate weather data"""
    return {
        "id": uuid.uuid4(),
        "device_id": device_id,
        "timestamp": timestamp,
        "location": location,
        "temperature": random.uniform(10, 30),
        "weatherCondition": random.choice(["Sunny", "Cloudy", "Rainy", "Foggy"]),
        "precipitation": random.uniform(0, 20),
        "windSpeed": random.uniform(0, 50),
        "humidity": random.randint(10, 90),  # percentage
        "airQualityIndex": random.uniform(0, 200),  # AQL value goes here
    }

def generate_emergency_incident_data(device_id, timestamp, location):
    """Simulate data for an emergency incident"""
    return {
        "id": uuid.uuid4(),
        "device_id": device_id,
        "incident_id": uuid.uuid4(),
        "type": random.choice(["Accident", "Fire", "Medical", "Police"]),
        "timestamp": timestamp,
        "location": location,
        "status": random.choice(["Active", "Resolved"]),
        "description": "Description of the incident",
    }

def simulate_vehicle_movement():
    """Simulate the movement of a vehicle"""
    global start_location
    # Move towards San Francisco
    start_location["latitude"] += LATITUDE_INCREMENT
    start_location["longitude"] += LONGITUDE_INCREMENT

    # Add some randomness to simulate actual road travel
    start_location["latitude"] += random.uniform(-0.0005, 0.0005)
    start_location["longitude"] += random.uniform(-0.0005, 0.0005)

    return start_location

def generate_vehicle_data(device_id):
    """Simulate vehicle data including location, speed, and vehicle details"""
    location = simulate_vehicle_movement()

    return {
        "id": uuid.uuid4(),
        "device_id": device_id,
        "timestamp": get_next_time().isoformat(),
        "location": (location["latitude"], location["longitude"]),
        "speed": random.uniform(0, 40),
        "direction": "North-East",
        "make": "Tesla",
        "model": "Model S",
        "year": 2024,
        "fuelType": "Electric",
    }

def json_serializer(obj):
    """Serializer to handle UUID objects for JSON serialization"""
    if isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def delivery_report(err, msg):
    """Callback for Kafka message delivery reports"""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_data_to_kafka(producer, topic, data):
    """Produce data to Kafka topic"""
    producer.produce(
        topic,
        key=str(data["id"]),
        value=json.dumps(data, default=json_serializer).encode("utf-8"),
        on_delivery=delivery_report
    )
    producer.flush()

def simulate_journey(producer, device_id):
    """Simulate a vehicle journey and produce data to Kafka topics"""
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        gps_data = generate_gps_data(device_id, vehicle_data["timestamp"])
        traffic_camera_data = generate_traffic_camera_data(
            device_id,
            vehicle_data["timestamp"],
            vehicle_data["location"],
            "Nikon-Cam123",
        )
        weather_data = generate_weather_data(
            device_id, vehicle_data["timestamp"], vehicle_data["location"]
        )
        emergency_incident_data = generate_emergency_incident_data(
            device_id, vehicle_data["timestamp"], vehicle_data["location"]
        )

        # Check if the vehicle has reached San Francisco
        if (
            vehicle_data["location"][0] >= SAN_FRANCISCO_COORDINATES["latitude"]
            and vehicle_data["location"][1] <= SAN_FRANCISCO_COORDINATES["longitude"]
        ):
            print("Vehicle has reached San Francisco. Exiting simulation.")
            break

        # Produce data to respective Kafka topics
        produce_data_to_kafka(producer, VEHICLE_TOPIC, vehicle_data)
        produce_data_to_kafka(producer, GPS_TOPIC, gps_data)
        produce_data_to_kafka(producer, TRAFFIC_TOPIC, traffic_camera_data)
        produce_data_to_kafka(producer, WEATHER_TOPIC, weather_data)
        produce_data_to_kafka(producer, EMERGENCY_TOPIC, emergency_incident_data)

        time.sleep(5)  # Wait for 5 seconds before generating new data

if __name__ == "__main__":
    producer_config = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "error_cb": lambda err: print(f"Kafka error: {err}"),
    }
    producer = SerializingProducer(producer_config)

    try:
        simulate_journey(producer, "Vehicle-DataSensei-123")
    except KeyboardInterrupt:
        print("Simulation stopped by user.")
    except Exception as e:
        print(f"Unexpected Error: {e}")
