
#importing required tools such as see and random 
import random
import numpy as np
from config import RANDOM_SEED
#pulling from helpers file, split for better organization
from helpers import export_records_csv, run_case

def summarize_comparison(results, num_cashiers):
	#prints the conditions ie number of customers and cashiers involved, i made it so cashiers is dynamic and based on user input
	print(f"\nComparative analysis ({num_cashiers}cashier(s) for three different scenarios including 20, 40, and 60 customers injected into the system)")
	#using a for loop to iterate through 20, 40, 60
	for case_size in [20, 40, 60]:
		metrics = results[case_size]
#prints off key metrics
		print(
			f"Case {case_size}: "
			f"The average wait time is {metrics['avg_waiting_time']:.4f}, "
			f"The average time in system is {metrics['avg_time_in_system']:.4f}, "
			f"The probability of waiting is {metrics['probability_of_waiting']:.4f}, "
			f"The cashier utilization is {metrics['cashier_utilization']:.4f}, "
			f"The idle time percentage is {metrics['idle_time_percentage']:.4f}"
		)
#this is to analyze the average waiting time differences moving from lower traffic scenarios to higher traffic scenarios and the differentials in between
	low_traffic = results[20]
	medium_traffic = results[40]
	high_traffic = results[60]
	print("\nCongestion Metric:")
	print(
		f"20 to 40 customers: Waiting increased by {medium_traffic['avg_waiting_time']-low_traffic['avg_waiting_time']:.4f} minutes, "
		f"Time in system increased by {medium_traffic['avg_time_in_system']-low_traffic['avg_time_in_system']:.4f} minutes"
	)
	print(
		f"40 to 60 customers: Waiting increased by {high_traffic['avg_waiting_time']-medium_traffic['avg_waiting_time']:.4f} minutes, "
		f"Time in system increased by {high_traffic['avg_time_in_system']-medium_traffic['avg_time_in_system']:.4f} minutes"
	)
	print(
		f"20 to 60 customers: Waiting increased by {high_traffic['avg_waiting_time']-low_traffic['avg_waiting_time']:.4f} minutes, "
		f"Time in system increased by {high_traffic['avg_time_in_system']-low_traffic['avg_time_in_system']:.4f} minutes"
	)

def get_cashier_count():
	#ask user how many cashiers to test but defaults to 1 to fulfill requirements
	try:
		value = input("Please input the number of cashiers simulated: ").strip()
		if not value:
			print("Defaults to 1 cashier.")
			return 1
		num_cashiers = int(value)
		if num_cashiers < 1:
			print("Defaults to 1 cashier.")
			return 1
		return num_cashiers
	except ValueError:
		print("Defaults to 1 cashier.")
		return 1

def main():
	random.seed(RANDOM_SEED)
	np.random.seed(RANDOM_SEED)
	num_cashiers = get_cashier_count()  # generates 20, 40 60 customer cases 
	results: dict[int, dict[str, float]] = {}
	#for loop to iterate through the cases 20,40,60
	for case_size in [20, 40, 60]:
		records, metrics = run_case(case_size, num_cashiers=num_cashiers)
		print(f"Case {case_size} metrics: " f"num_customers={metrics['num_customers']:.4f}, " f"avg_waiting_time={metrics['avg_waiting_time']:.4f}, "
			f"avg_time_in_system={metrics['avg_time_in_system']:.4f}, " f"probability_of_waiting={metrics['probability_of_waiting']:.4f}, "f"cashier_utilization={metrics['cashier_utilization']:.4f}, "
			f"idle_time={metrics['idle_time']:.4f}, " f"idle_time_percentage={metrics['idle_time_percentage']:.4f}"
		)
		#used for exporting csv
		export_records_csv(records, f"case_{case_size}_{num_cashiers}cashier.csv")
		results[case_size] = metrics
	summarize_comparison(results, num_cashiers)



if __name__ == "__main__":
	main()







