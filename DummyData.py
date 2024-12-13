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
high_threshold = 26417.205  
#thresholds for determining if fuel is low medium or high)
low_threshold = high_threshold/3.0
med_threshold = low_threshold *2.0


# fuel consumption in gallons per mile
fuelBurnRate = 5 

# generating arrival times using poisson 
interArrivals = np.random.exponential(1 / lambdaRate, numPlanes)
airportArrivals = np.cumsum(interArrivals)

# assigning initial plane distances between 100 and 500 miles away from airport
airportDistances = np.random.uniform(100, 500, numPlanes)

# calculating current fuel levels
fuelLevels = high_threshold - (airportDistances * fuelBurnRate)

# generating fake flight numbers
flight_ids = list()
for i in range(1, len(airportArrivals) + 1):
    flight_id = f"FL{str(i)}"
    flight_ids.append(flight_id) 

def truncate_float(num, decimals=3):
    """
    Function to truncate floats to make output more readable
    """
    factor = 10 ** decimals
    return trunc(num * factor) / factor


#to determine if our fuel level is low, med, high WE MAY NOT NEED
def classify_fuel(fuel_amount): 
    if fuel_amount < low_threshold:
        return "LOW"
    elif fuel_amount < med_threshold:
        return "MED"
    else:
        return "HIGH"


def getFlights(ids, arrivals, distances, fuel):
    """
    Returns a list of dummy data flights along with their poisson calculations
    """
    flights = []
    for i in range(numPlanes):
        # getting rid of np.float64() and truncating
        flights.append({"plane_