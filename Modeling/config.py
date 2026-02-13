"""Simulation configuration and distributions."""
import random
import numpy as np

# Random seed impacts all subsequent calls
RANDOM_SEED = 50
# Store hours in minutes (9 hours)
HOURS_OPEN = 9 * 60

# Interarrival time bounds(minutes)
INT_MIN = 1
INT_MAX = 10

# Discrete cashier service-time assumptions (minutes) and probabilities.
# More realistic than the original arbitrary setting: most transactions are
# completed in 3-5 minutes, with fewer short/long outliers.
SERVICE_TIME_VALUES = [2, 3, 4, 5, 6, 8]
SERVICE_TIME_PROBABILITIES = [0.08, 0.22, 0.30, 0.22, 0.13, 0.05]

def interarrival_time():
	# returns time between customer arrivals (uniform between 1-10 minutes)
	return random.uniform(INT_MIN, INT_MAX)

def service_time():
	# returns how long it takes to serve a customer (discrete distribution)
	return float(np.random.choice(SERVICE_TIME_VALUES, p=SERVICE_TIME_PROBABILITIES))
