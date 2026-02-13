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

def interarrival_time() -> float:
	"""Return interarrival time in minutes, this is generated using the min and max previously 
	defined ie 1 to 10 mins and uses a uniform distribution making each event equiprobable
	"""
	return random.uniform(INT_MIN, INT_MAX)

#randomixzed service time
def service_time() -> float:
	"""Return one sampled cashier service time in minutes (discrete distribution)."""
	return float(np.random.choice(SERVICE_TIME_VALUES, p=SERVICE_TIME_PROBABILITIES))
