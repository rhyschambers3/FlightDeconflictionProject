import numpy as np

# Peak Hours: During busy periods, LAX can accommodate around 60-80 landings per hour across its four runways.

# average arrivals per hour at LAX
lambda_rate = 70
 # simulate 100 plane arrivals
num_planes = 200

interarrival_times = np.random.exponential(1 / lambda_rate, num_planes)
# cumsum gets all of the cumilative arrival times
arrival_times = np.cumsum(interarrival_times)
