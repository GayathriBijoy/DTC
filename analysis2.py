import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from CSV files
shapes_df = pd.read_csv('raw_data/shapes.csv')
stops_df = pd.read_csv('raw_data/stops.csv')
trips_df = pd.read_csv('raw_data/trips.csv')

# 1. Plot Route Shape
def plot_route_shape(shape_id):
    shape_data = shapes_df[shapes_df['shape_id'] == shape_id]
    plt.figure(figsize=(8, 6))
    plt.plot(shape_data['shape_pt_lon'], shape_data['shape_pt_lat'], marker='o', color='b', label='Route Shape')
    plt.title(f'Route Shape for {shape_id}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.show()

# Plot the route for a particular shape_id
plot_route_shape('shp_1_2')

# 2. Plot Stop Locations
plt.figure(figsize=(8, 6))
plt.scatter(stops_df['stop_lon'], stops_df['stop_lat'], color='r', label='Bus Stops')
plt.title('Bus Stop Locations')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend()
plt.show()

# 3. Number of Trips per Route
trips_per_route = trips_df.groupby(['route_id', 'service_id']).size().reset_index(name='trip_count')

plt.figure(figsize=(10, 6))
sns.barplot(x='route_id', y='trip_count', hue='service_id', data=trips_per_route)
plt.title('Number of Trips per Route and Service Type')
plt.xlabel('Route ID')
plt.ylabel('Trip Count')
plt.show()
