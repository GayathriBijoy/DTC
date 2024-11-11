import requests
from gtfs_realtime_pb2 import FeedMessage  # Import the generated class from gtfs_realtime_pb2.py
import pandas as pd
from datetime import datetime

# API Key and URL for real-time data
api_key = "Bx84P7w0cmt3L8HAfNcFPTpvA30aPiOh"

url = f"https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key={api_key}"

# Load static data (Update paths as needed)
trips = pd.read_csv("raw_data/trips.csv")
stop_times = pd.read_csv("raw_data/stop_time.csv")
routes = pd.read_csv("raw_data/routes.csv")

try:
    # Step 1: Fetch Real-Time Data
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors

    # Parse protobuf data
    feed = FeedMessage()
    feed.ParseFromString(response.content)

    # Step 2: Parse vehicle data from protobuf
    vehicle_data = []
    for entity in feed.entity:
        if entity.HasField("vehicle"):
            vehicle = entity.vehicle
            vehicle_info = {
                "Vehicle_ID": vehicle.vehicle.id,
                "Current Status": vehicle.current_status,
                "Position Latitude": getattr(vehicle.position, "latitude", None),
                "Position Longitude": getattr(vehicle.position, "longitude", None),
                "Timestamp": vehicle.timestamp
            }
            vehicle_data.append(vehicle_info)

    # Step 3: Convert real-time data to DataFrame
    real_time_df = pd.DataFrame(vehicle_data)
    real_time_df['real_time'] = pd.to_datetime(real_time_df['Timestamp'], unit='s')

    # Step 4: Ensure Consistent Data Types for Merging
    trips['trip_id'] = trips['trip_id'].astype(str)
    stop_times['trip_id'] = stop_times['trip_id'].astype(str)
    real_time_df['trip_id'] = real_time_df['Vehicle_ID'].astype(str)  # Assuming Vehicle_ID corresponds to trip_id

    # Step 5: Merge Static Data
    # Merge stop_times and trips to link trips with routes
    trip_schedule = stop_times.merge(trips[['trip_id', 'route_id']], on='trip_id', how='left')
    
    # Check for missing route_id after merging stop_times and trips
    missing_route_ids = trip_schedule[trip_schedule['route_id'].isna()]
    if not missing_route_ids.empty:
        print("Warning: Some trip_ids in stop_times are not found in trips.csv. Missing route_ids:")
        print(missing_route_ids['trip_id'].unique())

    # Merge with routes to get route details
    trip_schedule = trip_schedule.merge(routes[['route_id', 'route_long_name']], on='route_id', how='left')

    # Step 6: Merge Real-Time Data with Trip Schedule
    # Now merge real-time data with trip schedule data on trip_id
    merged_data = real_time_df.merge(trip_schedule[['trip_id', 'route_id', 'arrival_time']], on='trip_id', how='left')

    # Check for missing route_ids in the final merged data
    if merged_data['route_id'].isna().any():
        print("Error: route_id is missing for some records after merging. Check for issues in trip_id values.")

    # Step 7: Calculate Delay in minutes
    def calculate_delay(row):
        try:
            scheduled_time = datetime.strptime(row['arrival_time'], '%H:%M:%S')
            real_time = row['real_time']
            delay = (real_time - scheduled_time).total_seconds() / 60
            return delay if delay > 0 else 0
        except (ValueError, TypeError):
            return None  # Return None if there’s an error in calculation

    merged_data['delay'] = merged_data.apply(calculate_delay, axis=1)

    # Step 8: Compute Average Delay per Route
    average_delay_per_route = merged_data.groupby('route_id')['delay'].mean()

    # Display the result
    print("\nAverage delay per route (in minutes):")
    print(average_delay_per_route)

except requests.exceptions.RequestException as e:
    print("Error fetching data from API:", e)
except Exception as e:
    print("An error occurred:", e)