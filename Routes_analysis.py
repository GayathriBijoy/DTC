import pandas as pd

# Load the CSV file
df = pd.read_csv('raw_data/routes.csv')

# Calculate the total number of routes
total_routes = df.shape[0]

print("Total number of routes:", total_routes)


#-----------------------------------------------------------

# Load the CSV data
routes_df = pd.read_csv('raw_data/routes.csv')
trips_df = pd.read_csv('raw_data/trips.csv')

# Calculate the number of trips per route
trips_per_route = trips_df['route_id'].value_counts()

# Calculate average, minimum, and maximum number of trips per route
avg_trips = trips_per_route.mean()
min_trips = trips_per_route.min()
max_trips = trips_per_route.max()

# Display high-demand routes (routes with more than the average number of trips)
high_demand_routes = trips_per_route[trips_per_route > avg_trips].index.tolist()

print("Average number of trips per route:", avg_trips)
print("Minimum number of trips per route:", min_trips)
print("Maximum number of trips per route:", max_trips)
print("High demand routes:", high_demand_routes)

# Assuming an operational cost model (for illustration purposes)
# You can replace this with your cost model if you have specific data
# For example: Assume cost per trip is a constant (e.g., 100 units)
cost_per_trip = 100
operational_costs = trips_per_route * cost_per_trip

# Calculate average, minimum, and maximum operational cost
avg_operational_cost = operational_costs.mean()
min_operational_cost = operational_costs.min()
max_operational_cost = operational_costs.max()

print("Average operational cost per route:", avg_operational_cost)
print("Minimum operational cost per route:", min_operational_cost)
print("Maximum operational cost per route:", max_operational_cost)
