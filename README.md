# PADCS

**A Personalized Adaptive Destructive-Constructive Search (PADCS) - Personalized Travel Itinerary Optimization**

> Thesis project - Faculty of Information Technology, VNU University of Engineering and Technology

## Overview

This system solves the **Team Orienteering Problem with Time Windows (TOPTW)** with user-dependent scoring. Unlike classic TOPTW where each POI has a fixed profit, our model computes personalized scores based on user preferences across 6 interest categories, subject to budget and time window constraints.

The solver implements a **Personalized Adaptive Destructive-Constructive Search (PADCS)** - a Genetic Algorithm hybridized with local search operators - exposed via a REST API.

## Algorithm Design

| Component | Details |
|---|---|
| **Encoding** | Permutation of POI IDs (depot-sandwiched) |
| **Initialization** | 80% Randomized Insertion Heuristic + 20% Pure Random |
| **Selection** | Tournament Selection (k=3) |
| **Crossover** | Order Crossover (OX1) |
| **Mutation** | Adaptive-Lite 3-operator: 2-opt, Swap, Insertion |
| **Local Search** | Smart Repair (remove worst score/time POI) + Greedy Refill |
| **Replacement** | (μ+λ) Merged Elitist with duplicate elimination |
| **Stopping** | Early stopping after 25 stagnant generations |

### Key Features

- **User-Dependent Scoring**: POI scores weighted by 6 interest categories (1-5 stars each)
- **Budget Constraint**: Ticket prices per POI category, based on Hanoi tourism statistics
- **Adaptive Mutation**: Operator probabilities shift dynamically based on search progress, diversity, and insertion failure rate
- **Ablation-Ready**: Every component can be toggled on/off for controlled experiments

## Interest Categories

| Category | Description | Example (Hanoi) |
|---|---|---|
| `history_culture` | Historical & cultural sites | Temple of Literature, Ho Chi Minh Mausoleum |
| `nature_parks` | Nature & parks | Hoan Kiem Lake, West Lake |
| `food_drink` | Food & dining | Old Quarter street food, Bun Cha |
| `shopping` | Shopping & markets | Dong Xuan Market |
| `entertainment` | Entertainment venues | Cinema, Opera House |
| `nightlife_wellness` | Nightlife & wellness | Ta Hien Street, Spa, Night market |

## Project Structure

```
PADCS/
├── src/
│   ├── main.py                     # FastAPI entry point
│   ├── api/                        # API routes
│   ├── core/                       # Configurations & Constants
│   ├── models/                     # Pydantic & Domain models
│   ├── services/                   # Logic & Data loading
│   │   ├── algorithm/              # Memetic Algorithm core
│   │   │   ├── padcs_engine.py      # Main loop
│   │   │   ├── initialization.py   # Init strategies
│   │   │   ├── fitness.py          # Fitness & Constraints
│   │   │   └── operators/          # GA Operators (OX1, 2-opt, Repair)
│   │   └── data_loader.py          # Solomon instance loader
│   ├── data/                       # Solomon benchmark datasets
│   └── experiments/                # Research scripts & Results
```

## API

### `POST /api/optimize`

**Request:**

```json
{
  "instance_name": "C101",
  "budget": 500000,
  "start_time": 8.0,
  "end_time": 17.0,
  "start_node_id": 0,
  "interests": {
    "history_culture": 5,
    "nature_parks": 3,
    "food_drink": 4,
    "shopping": 1,
    "entertainment": 2,
    "nightlife_wellness": 3
  }
}
```

**Response:** Optimized itinerary with total score, cost, distance, duration, execution time, and a detailed ordered list of POIs with arrival/departure times.

Interactive API docs available at `http://localhost:8000/docs` after starting the server.

## Getting Started

### Prerequisites

- Python 3.11+

### Install & Run

```bash
pip install -r requirements.txt
cd src
uvicorn main:app --reload
```

Server runs at `http://localhost:8000`.

### Run Experiments

```bash
cd src

# Generate extended dataset (category + price)
py -m experiments.generate_extended_data

# Benchmark vs Labadie (2012) - 30 runs × 6 instances
py -m experiments.exp1_benchmark

# Personalization value - 10 runs × 5 profiles
py -m experiments.exp2_personalization

# Budget impact - 10 runs × 3 tiers
py -m experiments.exp3_budget_impact

# Ablation study - 10 runs × 3 variants × 6 instances
py -m experiments.exp4_ablation_repair

# Parameter sensitivity - 5 runs × 16 configs × 6 instances
py -m experiments.exp5_sensitivity

# Analyze & plot
py -m experiments.analyze_results
py -m experiments.plot_charts
```

## Benchmark Results (Solomon TOPTW)

Comparison with Labadie et al. (2012) GVNS on 6 Solomon instances, single-vehicle (m=1).

## License

Distributed under the MIT License. See `LICENSE` for details.

## Author

**Hoang Minh Duc** - Faculty of Information Technology, VNU University of Engineering and Technology (VNU-UET)
