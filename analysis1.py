import matplotlib.pyplot as plt
import pandas as pd 
#from sklearn.cluster import KMeans
from geopy.distance import geodesic
import folium

df = pd.read_csv('raw_data/shapes.csv')

"""
# Initialize map centered on the first stop
m = folium.Map(location=[df['stop_lat'][0], df['stop_lon'][0]], zoom_start=12)

# Add markers for each stop
for i, row in df.iterrows():
    folium.Marker([row['stop_lat'], row['stop_lon']], popup=row['stop_name']).add_to(m)

# Display the map
m.save('my_map.html')

#distance between 2 stops 

from geopy.distance import geodesic
# Function to find the closest stops
def find_closest_stops(stop_name, df, num_stops=5):
    # Check if the stop exists in the DataFrame
    if stop_name not in df['stop_name'].values:
        print(f"Stop name '{stop_name}' not found in the dataset.")
        return
    
    # Get the latitude and longitude of the input stop
    stop_info = df[df['stop_name'] == stop_name]
    stop_lat = stop_info['stop_lat'].values[0]
    stop_lon = stop_info['stop_lon'].values[0]
    stop_coords = (stop_lat, stop_lon)

    # Calculate the distance from the input stop to all other stops
    distances = []
    for i, row in df.iterrows():
        current_coords = (row['stop_lat'], row['stop_lon'])
        distance = geodesic(stop_coords, current_coords).kilometers
        distances.append((row['stop_name'], distance))

    # Sort the distances (excluding the input stop itself) and get the closest ones
    distances = sorted(distances, key=lambda x: x[1])
    closest_stops = [stop for stop in distances if stop[0] != stop_name][:num_stops]
    
    # Print the closest stops
    print(f"Closest {num_stops} stops to '{stop_name}':")
    for stop, distance in closest_stops:
        print(f"{stop}: {distance:.2f} km")

# Example usage
stop_name = input("Enter the stop name: ")  # Input stop name
find_closest_stops(stop_name, df, num_stops=5)

"""

"""

#cluster analysis-------------

coordinates = df[['stop_lat', 'stop_lon']]
kmeans = KMeans(n_clusters=3).fit(coordinates)
df['cluster'] = kmeans.labels_
#visualisation of cluster analysis 
# Plotting clusters
plt.scatter(df['stop_lon'], df['stop_lat'], c=df['cluster'], cmap='viridis')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Transit Stops Clustering')
plt.show()
"""
#stop distribution ---------------------------------
"""
plt.scatter(df['stop_lon'], df['stop_lat'])
plt.title("Stop Distribution")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
#---------------------------------------------------
"""
# stops in shapes 

import pandas as pd
from geopy.distance import geodesic

# Load the data from CSV files
stops_df = pd.read_csv('raw_data/stops.csv')
shapes_df = pd.read_csv('raw_data/shapes.csv')
trips_df = pd.read_csv('raw_data/trips.csv')

# Function to find the closest shape_id for a given stop name
def find_shape_by_stop(stop_name):
    # Search for the stop name in the stops dataframe
    stop_info = stops_df[stops_df['stop_name'].str.lower() == stop_name.lower()]
    
    if not stop_info.empty:
        # Extract stop latitude and longitude
        stop_lat = stop_info['stop_lat'].values[0]
        stop_lon = stop_info['stop_lon'].values[0]
        
        # Find the closest shape point by comparing distances
        min_distance = float('inf')
        closest_shape_id = None
        
        for _, row in shapes_df.iterrows():
            shape_lat = row['shape_pt_lat']
            shape_lon = row['shape_pt_lon']
            
            # Calculate the geodesic distance between the stop and the shape point
            distance = geodesic((stop_lat, stop_lon), (shape_lat, shape_lon)).meters
            
            if distance < min_distance:
                min_distance = distance
                closest_shape_id = row['shape_id']
        
        return stop_lat, stop_lon, closest_shape_id
    else:
        return None, None, "Stop not found."

def count_trips_and_routes(stop_name):
    stop_lat, stop_lon, closest_shape_id = find_shape_by_stop(stop_name)
    
    if closest_shape_id == "Stop not found.":
        print("Stop not found.")
        return

    trips_count = trips_df[trips_df['shape_id'] == closest_shape_id].shape[0]
    
    
    unique_routes_count = trips_df[trips_df['shape_id'] == closest_shape_id]['trip_id'].nunique()
    
    #routes_count = trips_df[trips_df['shape_id'] == closest_shape_id]['trip_id']

    print(f"Stop: {stop_name}")
    print(f"Closest Shape ID: {closest_shape_id}")
    print(f"Number of Trips: {trips_count}")
    print(f"Number of Unique Routes: {unique_routes_count}")
    #print(f"Number of Routes: {routes_count}")

stop_name_input = input("Enter the stop name: ")
count_trips_and_routes(stop_name_input)