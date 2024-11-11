# API KEY - Bx84P7w0cmt3L8HAfNcFPTpvA30aPiOh
import requests
from gtfs_realtime_pb2 import FeedMessage  # Import the generated class from gtfs_realtime_pb2.py
import pandas as pd 


api_key = "Bx84P7w0cmt3L8HAfNcFPTpvA30aPiOh"

url = f"https://otd.delhi.gov.in/api/realtime/VehiclePositions.pb?key={api_key}"

try:
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors

    # Parse the protobuf data
    feed = FeedMessage()
    feed.ParseFromString(response.content)

    vehicle_data =[]


    
    # Output the vehicle positions
    for entity in feed.entity:
        if entity.HasField("vehicle"):
            vehicle = entity.vehicle
            vehicle_info = {
            "Vehicle_ID": vehicle.vehicle.id,
            "Current Status" : vehicle.current_status,
            "Position Latitude" :  vehicle.position.latitude,
            "Position Longitude" : vehicle.position.longitude,
            "Timestamp" : vehicle.timestamp}
        
        vehicle_data.append(vehicle_info)

    df = pd.DataFrame(vehicle_data)

    print(df)
    
    #pre process location col
    df = df[(df["Position Latitude"] > 0) & (df["Position Longitude"] > 0) ]
    #print(df[df["Position Latitude"]])
    
    print(df.shape)


   
    # no of electric vehicles 
    no_of_electric_vehicles = df[df['Vehicle_ID'].str.contains("EV")].shape
    print(f'no of electric vehicles {no_of_electric_vehicles[0]}')

    # no of fossil fuel vehicles 
    total_vehicles = df.shape
    no_of_ff_vehicles = total_vehicles[0] - no_of_electric_vehicles[0]
    print(f'no_of_ff_vehicles is {no_of_ff_vehicles}')
    
    print(f'sum = {no_of_ff_vehicles + no_of_electric_vehicles[0]}')

  

    
    






except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as err:
    print(f"Request error occurred: {err}")
except Exception as e:
    print(f"An error occurred: {e}")