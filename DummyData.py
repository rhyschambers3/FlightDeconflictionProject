import numpy as np
from math import trunc

"""
This program calculates the poisson distriubtion of arriving to an airport once program starts
In the end of a program we get a list of fake flights that have an estimated time of arrival, distance from airport, and fuel amount
    The flight information is stored in a dictionary with keys that are as follows
    flights: planes and their data (tuples)
        "plane_id": plane id
       "eta_arr" : hours until arrival to airport
        "dist": distance from airport (miles)
       "fuel": fuel level in relation to a start that was randomly calculated above
Simulation Parameters: found online for the average numbers 
"""
 
# during peak time 60-80 arrivals per hour for all four runways at LAX, so taking the average here
lambdaRate = 70 # our lambda rate is the average number of plane arrivals at LAX
 # want to model 100 planes landing
numPlanes = 100
# initial fuel in gallons
high_threshold = 5800  
#thresholds for determining if fuel is low medium or high)
low_threshold = 5500
med_threshold = 5600


# fuel consumption in gallons per mile
fuelBurnRate = 1

# generating arrival times using poisson 
interArrivals = np.random.exponential(1 / lambdaRate, numPlanes)
airportArrivals = np.cumsum(interArrivals)

# assigning initial plane distances between 100 and 500 miles away from airport
airportDistances = np.random.uniform(100, 500, numPlanes)

# calculating current fuel levels
fuelLevels = high_threshold - (airportDistances * fuelBurnRate)

# generating fake flight numbers
flight_ids = list()
for i in range(1, 25):
    flight_id = f"AA{str(i)}"
    flight_ids.append(flight_id) 
for i in range(25, 50):
    flight_id = f"JB{str(i)}"
    flight_ids.append(flight_id) 
for i in range(50, 60):
    flight_id = f"AF{str(i)}"
    flight_ids.append(flight_id) 
for i in range(60, 75):
    flight_id = f"DL{str(i)}"
    flight_ids.append(flight_id) 
for i in range(75, 80):
    flight_id = f"SP{str(i)}"
    flight_ids.append(flight_id) 
for i in range(80, 100):
    flight_id = f"AC{str(i)}"
    flight_ids.append(flight_id) 

def truncate_float(num, decimals=3):
    """
    Function to truncate floats to make output more readable
    """
    factor = 10 ** decimals
    return trunc(num * factor) / factor


#to determine if our fuel level is low, med, high WE MAY NOT NEED
def classify_fuel(fuel_amount): 
    if fuel_amount > med_threshold:
        return "HIGH"
    
    if fuel_amount > low_threshold and fuel_amount < med_threshold:
        return "MEDIUM"
    # elif fuel_amount < med_threshold:
    #     return "LOW"
    else:
        return "LOW"


def getFlights(ids, arrivals, distances, fuel):
    """
    Returns a list of dummy data flights along with their poisson calculations
    """
    flights = []
    for i in range(1,numPlanes-1):
        # getting rid of np.float64() and truncating
        flights.append({"id": ids[i], "distance": truncate_float(distances[i],3), "fuel": truncate_float(fuel[i],3), "classify": classify_fuel(truncate_float(fuel[i],3))})
        # flights.append((ids[i], truncate_float(arrivals[i],3), truncate_float(distances[i],3), truncate_float(fuel[i],3)))
    return flights

# can take first 20 or so of these to get planes that are arriving soon
flights = getFlights(flight_ids, airportArrivals, airportDistances, fuelLevels)

# can uncomment to get outputs
# for flight in flights:
#    print(f"{flight['id']} hours\n    Distance from airport: {flight['distance']} miles\n    With a fuel level of: {flight['fuel']} gallons\n     fuel level is: {flight['classify']}")
