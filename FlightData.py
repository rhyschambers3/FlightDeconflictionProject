from pyflightdata import FlightData
from datetime import datetime, timedelta
import pytz

# Initialize FlightData
f = FlightData()

# Define parameters
airport_code = "KLAX"
target_time = datetime.utcnow()

# convert UTC to LA local time
los_angeles_tz = pytz.timezone('America/Los_Angeles')
target_time_la = target_time.astimezone(los_angeles_tz)
print(f"Target time in Los Angeles local time: {target_time_la}")

# Time window for 60 minutes
time_window = 300  # 60 minutes before or after current time

# getting current time in LA
start_time_la = target_time_la - timedelta(minutes=time_window)
end_time_la = target_time_la + timedelta(minutes=time_window)

# Print the start and end times in Los Angeles local time
print(f"Start time in Los Angeles: {start_time_la}")
print(f"End time in Los Angeles: {end_time_la}")

# Get arrivals for the airport
arrivals = f.get_airport_arrivals(airport_code, limit=100)

# fliter arrivals within our desired time rang of an hour
filtered_flights = []
for flight in arrivals:
    # print(flight['flight'].keys())
    if 'time' in flight['flight']:
        flight_info = flight['flight']
        # print("time is in flight")
        # accessing scheduled flight time
        arrival_time = flight_info['time']['scheduled']['arrival'] #we will be using sheduled arrivals because a lot of the real arrivals are none and this messes ish up

        # print(f"DEBUG: Flight {flight_info['identification']['number']['default']} - "
        #       f"Raw real arrival: {flight_info['time']['real']['arrival']}, "
        #       f"Raw scheduled arrival: {flight_info['time']['scheduled']['arrival']}")

        # If arrival_time is found, convert it to a datetime object
        if arrival_time:
            print(arrival_time)
            # Check if arrival_time is a valid value (not 'None' or any non-numeric string)
            if isinstance(arrival_time, str):
                arrival_time = int(arrival_time)  # Convert string to int
            arrival_time_utc = datetime.fromtimestamp(arrival_time, tz=pytz.utc)  # Ensure UTC time
            # print(f"Converted arrival time (UTC): {arrival_time_utc}")
            arrival_time_la = arrival_time_utc.astimezone(los_angeles_tz) #convert UTC to LA local time
            # print(f"Arrival time in Los Angeles local time: {arrival_time_la}")

            # check if the arrival time is within the defined time range
            if start_time_la <= arrival_time_la <= end_time_la:
                # arrival time is within our defined times rang
                filtered_flights.append(flight)
                print(f"Added to filtered flights: {flight_info['identification']['number']['default']}")

# Print results
if filtered_flights:
    print(f"number of Filtered flights are: {len(filtered_flights)}")
    
else:
    print("No flights found within the specified time window.")
