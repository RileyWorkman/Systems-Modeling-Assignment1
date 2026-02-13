
import random
import numpy as np
from config import RANDOM_SEED
from helpers import export_records_csv, run_case

def summarize_comparison(results, num_cashiers):
	print(f"\nComparative analysis ({num_cashiers} cashier(s), 20 vs 40 vs 60 customers)")
	for case_size in [20, 40, 60]:
		metrics = results[case_size]
		print(
			f"Case {case_size}: "
			f"avg_wait={metrics['avg_waiting_time']:.3f}, "
			f"avg_system={metrics['avg_time_in_system']:.3f}, "
			f"p_wait={metrics['probability_of_waiting']:.3f}, "
			f"utilization={metrics['cashier_utilization']:.3f}, "
			f"idle_pct={metrics['idle_time_percentage']:.3f}"
		)

	base = results[20]
	worst = results[60]
	print("\nSystem congestion trend:")
	print(
		f"Waiting increased by {worst['avg_waiting_time'] - base['avg_waiting_time']:.3f} "
		f"minutes from 20 to 60 customers."
	)
	print(
		f"Time in system increased by {worst['avg_time_in_system'] - base['avg_time_in_system']:.3f} "
		f"minutes from 20 to 60 customers."
	)

	# these are my thresholds for deciding if we have enough cashiers
	max_avg_wait = 5.0
	max_probability_wait = 0.50
	max_utilization = 0.90

	is_sufficient = (
		worst["avg_waiting_time"] <= max_avg_wait
		and worst["probability_of_waiting"] <= max_probability_wait
		and worst["cashier_utilization"] <= max_utilization
	)

	if is_sufficient:
		print(f"{num_cashiers} cashier(s) appears sufficient for tested loads.")
	else:
		print(f"{num_cashiers} cashier(s) appears insufficient for tested loads.")
		print(
			f"(Thresholds used: avg_wait <= {max_avg_wait}, "
			f"p_wait <= {max_probability_wait}, utilization <= {max_utilization})"
		)

def get_cashier_count():
	# ask user how many cashiers to test
	try:
		value = input("Enter number of cashiers (default 1): ").strip()
		if not value:
			return 1
		num_cashiers = int(value)
		if num_cashiers < 1:
			print("Invalid value. Using default: 1")
			return 1
		return num_cashiers
	except ValueError:
		print("Invalid value. Using default: 1")
		return 1

def main():
	random.seed(RANDOM_SEED)
	np.random.seed(RANDOM_SEED)
	num_cashiers = get_cashier_count()
	# 20, 40, 60 customer cases
	results: dict[int, dict[str, float]] = {}
	for case_size in [20, 40, 60]:
		records, metrics = run_case(case_size, num_cashiers=num_cashiers)
		print(f"Case {case_size} metrics: {metrics}")
		export_records_csv(records, f"case_{case_size}_{num_cashiers}cashier.csv")
		results[case_size] = metrics

	summarize_comparison(results, num_cashiers)

if __name__ == "__main__":
	main()







