import pandas as pd
import numpy as np
from datetime import datetime

# Load CSV files with example file paths (update with actual paths)
try:
    trips = pd.read_csv("raw_data/trips.csv")
    stop_times = pd.read_csv("raw_data/stop_time.csv")  # Corrected filename
    routes = pd.read_csv("raw_data/routes.csv")
    real_time_data = pd.read_csv("real_time_data.csv")  # assuming this file contains Vehicle_ID, Timestamp, etc.

    # Check the loaded data
    print("Trips Data Sample:")
    print(trips.head())
    print("\nStop Times Data Sample:")
    print(stop_times.head())
    print("\nRoutes Data Sample:")
    print(routes.head())
    print("\nReal-Time Data Sample:")
    print(real_time_data.head())
    
    # Ensure columns are of compatible types for merging
    trips['trip_id'] = trips['trip_id'].astype(str)
    stop_times['trip_id'] = stop_times['trip_id'].astype(str)
    
    # Merge stop_times and trips to link trips with routes
    trip_schedule = stop_times.merge(trips[['trip_id', 'route_id']], on='trip_id', how='left')
    trip_schedule = trip_schedule.merge(routes[['route_id', 'route_long_name']], on='route_id', how='left')

    # Debugging output
    print("\nMerged Trip Schedule Data Sample:")
    print(trip_schedule.head())

    # Prepare real-time data (assuming 'Timestamp' is in Unix time)
    real_time_data['real_time'] = pd.to_datetime(real_time_data['Timestamp'], unit='s')
    
    # Attempt to merge real-time data with trip schedule
    # Assuming 'trip_id' or another matching key is available; adjust if needed
    real_time_data['trip_id'] = real_time_data['Vehicle_ID'].astype(str)  # Example to add trip_id; adjust as needed
    real_time_data = real_time_data.merge(trip_schedule[['trip_id', 'route_id', 'arrival_time']], on='trip_id', how='left')

    # Debugging output
    print("\nReal-Time Data after merging with Trip Schedule:")
    print(real_time_data.head())

    # Calculate delay in minutes
    def calculate_delay(row):
        try:
            scheduled_time = datetime.strptime(row['arrival_time'], '%H:%M:%S')
            real_time = row['real_time']
            delay = (real_time - scheduled_time).total_seconds() / 60
            return delay if delay > 0 else 0
        except (ValueError, TypeError):
            return np.nan

    real_time_data['delay'] = real_time_data.apply(lambda row: calculate_delay(row), axis=1)

    # Debugging output for delay calculation
    print("\nReal-Time Data with Calculated Delays:")
    print(real_time_data[['trip_id', 'route_id', 'delay']].head())

    # Calculate average delay per route
    average_delay_per_route = real_time_data.groupby('route_id')['delay'].mean()

    # Display the result
    print("\nAverage delay per route (in minutes):")
    print(average_delay_per_route)

except FileNotFoundError as e:
    print("File not found:", e)
except Exception as e:
    print("An error occurred:", e)
