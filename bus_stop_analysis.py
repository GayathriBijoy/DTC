import pandas as pd

# Load the stops and stop_time data
stops_df = pd.read_csv('raw_data/stops.csv')
stop_time_df = pd.read_csv('raw_data/stop_time.csv')

# Total number of bus stops
total_bus_stops = stops_df['stop_id'].nunique()

# Count the number of visits per bus stop
visits_per_stop = stop_time_df['stop_id'].value_counts()

# Calculate average, minimum, and maximum visits per bus stop
avg_visits = visits_per_stop.mean()
min_visits = visits_per_stop.min()
max_visits = visits_per_stop.max()

# Output the results
print("Total number of bus stops:", total_bus_stops)
print("Average visits per bus stop:", avg_visits)
print("Minimum visits per bus stop:", min_visits)
print("Maximum visits per bus stop:", max_visits)
