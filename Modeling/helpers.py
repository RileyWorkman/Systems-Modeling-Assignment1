# Helper functions for simulation
import csv
import simpy
from Attributes import CustomerRecord, OUTPUT_COLUMNS
from config import interarrival_time, service_time

def customer_process(env, customer_id, cashier, records, interarrival):
	# this function handles a single customer going through the system
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
def arrival_process(env, cashier, num_customers, records, interarrival_fn):
	# generates customer arrivals - creates exactly the number of customers we want (20, 40, or 60)
	for customer_id in range(1, num_customers + 1):

		interarrival = interarrival_fn()
		yield env.timeout(interarrival)
		# start the customer process
		env.process(customer_process(env, customer_id, cashier, records, interarrival))

def run_case(num_customers, num_cashiers=1):
	# runs the simulation for one case (20, 40, or 60 customers)
	env = simpy.Environment()
	cashier = simpy.Resource(env, capacity=num_cashiers)
	records = []

	env.process(arrival_process(env, cashier, num_customers, records, interarrival_time))
	env.run()

	metrics = compute_metrics(records)
	return records, metrics

def compute_metrics(records):
	# calculate all the performance metrics from the customer records
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

def export_records_csv(records, filename):
	# write the customer records to a CSV file
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
