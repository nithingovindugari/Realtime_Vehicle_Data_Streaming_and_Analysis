# Realtime Vehicle Data Streaming and Analysis

This project simulates the movement of a vehicle from San Jose to San Francisco, generating various types of data (vehicle, GPS, traffic camera, weather, and emergency incident data) and sending it to Kafka topics. The data is then processed and analyzed using Apache Spark, AWS Glue, and Amazon Redshift for real-time insights and analysis.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Simulation](#running-the-simulation)
- [Architecture](#architecture)
- [File Descriptions](#file-descriptions)


## Overview
This project aims to collect and analyze real-time data from a vehicle traveling between San Jose and San Francisco. The data includes vehicle telemetry, GPS coordinates, weather conditions, traffic camera snapshots, and emergency incidents. The architecture leverages Apache Kafka for data streaming, Apache Spark for data processing, AWS Glue for ETL operations, and Amazon Redshift for data storage and analysis. Docker is used to set up the necessary services, including ZooKeeper and Kafka.

## Prerequisites
Before running the simulation, ensure you have the following installed:
- Python 3.7+
- Docker
- Docker Compose
- AWS account with necessary permissions for S3, Glue, and Redshift

## Installation
Clone the repository:
```bash
git clone https://github.com/your-username/realtime-vehicle-data-streaming.git
cd realtime-vehicle-data-streaming

# Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Build and start the Docker containers:
```bash
docker-compose up -d


## Configuration

# Ensure the following settings are correctly configured in your config.py file:

```bash
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
VEHICLE_TOPIC=vehicle_data
GPS_TOPIC=gps_data
TRAFFIC_TOPIC=traffic_data
WEATHER_TOPIC=weather_data
EMERGENCY_TOPIC=emergency_data
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
AWS_S3_BUCKET=spark-streaming-data
AWS_REDSHIFT_CLUSTER=your_redshift_cluster
AWS_REDSHIFT_DATABASE=your_redshift_database
AWS_REDSHIFT_USER=your_redshift_user
AWS_REDSHIFT_PASSWORD=your_redshift_password


## Running the Simulation

# To start the simulation, run the following command:
```bash
python main.py
```
This will start generating vehicle data and sending it to the Kafka topics. You can view the data using the Kafka console consumer:

## Architecture

The architecture includes the following components:

1) Data Generation: Simulated vehicle data, GPS location, weather info, and emergency information are generated in real-time.
2) Data Streaming: Data is streamed to Apache Kafka topics using Dockerized ZooKeeper and Kafka.
3) Data Processing: Apache Spark processes the streamed data, which is then sent to AWS S3 for storage.
4) ETL Operations: AWS Glue is used for ETL operations to transform and load the data into Amazon Redshift.
5) Data Storage and Analysis: Data is stored in Amazon Redshift and can be queried using Amazon Athena or visualized using PowerBI or Amazon QuickSight.


## File Descriptions

- main.py: The main simulation script that generates and sends synthetic data to Kafka topics.
- spark-vehicle.py: The script for processing and analyzing data using Apache Spark.
- docker-compose.yml: Docker Compose configuration for setting up the Kafka and Spark environment.
- config.py: Configuration file for AWS credentials and settings.
- requirements.txt: Python dependencies required for the project.
- README.md: This README file.








