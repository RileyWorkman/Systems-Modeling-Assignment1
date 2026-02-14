#Data models and constants for the simulation.

from dataclasses import dataclass
from typing import List

@dataclass
class CustomerRecord:
	#Per-customer event record. We can add to this if we choose to if we want more data


	customer_id: int
	interarrival_time: float
	arrival_time: float
	service_start_time: float
	service_time: float
	service_completion_time: float
	waiting_time: float
	time_in_system: float

OUTPUT_COLUMNS: List[str] = [
	"customer_id","interarrival_time","arrival_time","service_start_time","service_time",
	"service_completion_time","waiting_time","time_in_system",]

