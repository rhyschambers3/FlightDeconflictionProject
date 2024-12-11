import numpy as np
from math import trunc

"""
This program calculates the poisson distriubtion of arriving to an airport once program starts
In the end of a prgram we get a list of fake flights that have an estimated time of arrival, distance from airport, and fuel amount
    flights: planes and their data (tuples)
        Index 0: plane id
        Index 1: estimated time of arrival  to airpoirt (hours)
        Index 2: distance from airport (miles)
        Index 3: fuel level in relation to a start that was randomly calculated above
Simulation Parameters: found online for the average numbers 
"""

# during peak time 60-80 arrivals per hour for all four runways at LAX, so taking the average here
lambdaRate = 70 # our lambda rate is the average number of plane arrivals at LAX
 # want to model 100 planes landing
numPlanes = 100
# initial fuel in gallons
initialFuel = 26417.205  
# fuel consumption in gallons per mile
fuelBurnRate = 5 

# generating arrival times using poisson 
interArrivals = np.random.exponential(1 / lambdaRate, numPlanes)
airportArrivals = np.cumsum(interArrivals)

# assigning initial plane distances between 100 and 500 miles away from airport
airportDistances = np.random.uniform(100, 500, numPlanes)

# calculating current fuel levels
fuelLevels = initialFuel - (airportDistances * fuelBurnRate)

# generating fake flight numbers
flight_ids = [f"FL{str(i)}" for i in range(1, len(airportArrivals) + 1)]     

def truncate_float(num, decimals=3):
    """
    Function to truncate floats to make output more readable
    """
    factor = 10 ** decimals
    return trunc(num * factor) / factor

def getFlights(ids, arrivals, distances, fuel):
    """
    Returns a list of dummy data flights along with their poisson calculations
    """
    flights = []
    for i in range(numPlanes):
        # getting rid of np.float64() and truncating
        flights.append((ids[i], truncate_float(arrivals[i],3), truncate_float(distances[i],3), truncate_float(fuel[i],3)))
    return flights

# can take first 20 or so of these to get planes that are arriving soon
flights = getFlights(flight_ids, airportArrivals, airportDistances, fuelLevels)

# can uncomment to get outputs
# for flight in flights:
#     print(f"Flight Number: {flight[0]}\n    Arriving to airport in {flight[1]} hours\n    Distance from airpoirt: {flight[2]} miles\n    With fuel a fuel level of: {flight[3]} gallons")
