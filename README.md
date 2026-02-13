# Grocery Store Cashier Queue Simulation

Discrete event simulation modeling a grocery store checkout system with customer arrivals, queuing, and service.

## Requirements

- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/RileyWorkman/Systems-Modeling-Assignment1.git
   cd Systems-Modeling-Assignment1
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Simulation

```bash
python Modeling/main.py
```

This will:
- Run simulations for 20, 40, and 60 customers
- Generate CSV files with customer records
- Display performance metrics and comparative analysis

## Output Files

The simulation generates three CSV files:
- `case_20_1cashier.csv`
- `case_40_1cashier.csv`
- `case_60_1cashier.csv`

Each contains detailed records for every customer including arrival time, service time, waiting time, etc.

## Configuration

To change the number of cashiers, edit line 70 in `Modeling/main.py`:
```python
num_cashiers = 1  # change this value
```

## Project Structure

```
Modeling/
├── main.py          # Entry point - runs the simulation
├── helpers.py       # Simulation functions and metrics
├── config.py        # Configuration and probability distributions
├── Attributes.py    # Data models
```

## Assumptions

- **Interarrival time**: Uniform(1, 10) minutes
- **Service time**: Discrete distribution [2,3,4,5,6,8] minutes
- **Random seed**: 50 (for reproducibility)
