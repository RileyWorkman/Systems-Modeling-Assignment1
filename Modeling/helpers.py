"""Helpers consolidated
"""
from typing import Dict, Iterable, List, Tuple
import csv
import simpy
from Attributes import CustomerRecord, OUTPUT_COLUMNS
from config import interarrival_time, service_time

def customer_process(
		#defines environment ie simulation time and queue
	env: simpy.Environment,
	#customer id is an integer which is assigned to track
	customer_id: int,
	#simpy resource is used to model the cashiers availability
	cashier: simpy.Resource,
	#this lists the customer records
	records: List[CustomerRecord],
	#this is the time between consecutive events in minutes (ie between customer arrivals)
	interarrival: float,
	
) -> Iterable[simpy.events.Event]:
	"""SimPy process for a single customer such as iplement arrival, queueing, service, and record keeping.
	"""
	arrival_time = env.now
	with cashier.request() as request:
		yield request
		service_start_time = env.now
		sampled_service_time = service_time()
		yield env.timeout(sampled_service_time)
		service_completion_time = env.now

	waiting_time = service_start_time - arrival_time
	time_in_system = service_completion_time - arrival_time

	records.append(
		CustomerRecord(
			customer_id=customer_id,
			interarrival_time=interarrival,
			arrival_time=arrival_time,
			service_start_time=service_start_time,
			service_time=sampled_service_time,
			service_completion_time=service_completion_time,
			waiting_time=waiting_time,
			time_in_system=time_in_system,
		)
	)
def arrival_process(
	env: simpy.Environment,
	cashier: simpy.Resource,
	num_customers: int,
	#logs records
	records: List[CustomerRecord],
	interarrival_fn,
) -> Iterable[simpy.events.Event]:
	"""Generate arrivals for a fixed customer-count experiment.

	Note: The assignment cases are fixed at 20/40/60 customers, so this process
	creates exactly ``num_customers`` arrivals.
	"""
	for customer_id in range(1, num_customers + 1):

		interarrival = interarrival_fn()
		yield env.timeout(interarrival)
		env.process(
#customer process is an instances of a customer arriving and going through the designed system
			customer_process(
				env=env,
				customer_id=customer_id,
				cashier=cashier,
				records=records,
				interarrival=interarrival,
			)
		)

def run_case(num_customers: int, num_cashiers: int = 1) -> Tuple[List[CustomerRecord], Dict[str, float]]:
	"""Run a single simulation case and return records plus metrics."""
	env = simpy.Environment()
	cashier = simpy.Resource(env, capacity=num_cashiers)
	records: List[CustomerRecord] = []

	env.process(
		arrival_process(
			env=env,
			cashier=cashier,
			num_customers=num_customers,
			records=records,
			interarrival_fn=interarrival_time,
		)
	)
	env.run()

	metrics = compute_metrics(records)
	return records, metrics

def compute_metrics(records: List[CustomerRecord]) -> Dict[str, float]:
	"""Compute performance measures from records."""
	if not records:
		return {
			"num_customers": 0.0,
			"avg_waiting_time": 0.0,
			"avg_time_in_system": 0.0,
			"probability_of_waiting": 0.0,
			"cashier_utilization": 0.0,
			"idle_time": 0.0,
			"idle_time_percentage": 0.0,
		}

	num_customers = len(records)
	total_waiting = sum(r.waiting_time for r in records)
	total_time_in_system = sum(r.time_in_system for r in records)
	total_service_time = sum(r.service_time for r in records)
	customers_who_waited = sum(1 for r in records if r.waiting_time > 0)

	simulation_end_time = max(r.service_completion_time for r in records)
	if simulation_end_time > 0:
		cashier_utilization = total_service_time / simulation_end_time
		idle_time = simulation_end_time - total_service_time
		idle_time_percentage = idle_time / simulation_end_time
	else:
		cashier_utilization = 0.0
		idle_time = 0.0
		idle_time_percentage = 0.0

	return {
		"num_customers": float(num_customers),
		"avg_waiting_time": total_waiting / num_customers,
		"avg_time_in_system": total_time_in_system / num_customers,
		"probability_of_waiting": customers_who_waited / num_customers,
		"cashier_utilization": cashier_utilization,
		"idle_time": idle_time,
		"idle_time_percentage": idle_time_percentage,
	}

def export_records_csv(records: List[CustomerRecord], filename: str) -> None:
	"""Export records to CSV with OUTPUT_COLUMNS."""
	with open(filename, "w", newline="") as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_COLUMNS)
		writer.writeheader()
		for record in records:
			writer.writerow(
				{
					"customer_id": record.customer_id,
					"interarrival_time": round(record.interarrival_time, 3),
					"arrival_time": round(record.arrival_time, 3),
					"service_start_time": round(record.service_start_time, 3),
					"service_time": round(record.service_time, 3),
					"service_completion_time": round(record.service_completion_time, 3),
					"waiting_time": round(record.waiting_time, 3),
					"time_in_system": round(record.time_in_system, 3),
				}
			)
