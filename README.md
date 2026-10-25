# PADCS: Personalized Adaptive Destructive-Constructive Search

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+"/>
  <img src="https://img.shields.io/badge/FastAPI-0.128-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Solomon_TOPTW-100%25_BKS_Match-success?style=for-the-badge&logo=target&logoColor=white" alt="Benchmark"/>
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/VNU--UET-Graduation_Thesis-8A2BE2?style=for-the-badge" alt="UET Thesis"/>
</p>

---

## 🎬 Live Interactive Demo & Web Simulation

<p align="center">
  <a href="https://hm4uc.github.io/PADCS/" target="_blank">
    <img src="docs/assets/demo_preview.png" alt="PADCS AI Tour Planner UI" width="100%"/>
  </a>
</p>

<p align="center">
  <a href="https://hm4uc.github.io/PADCS/" target="_blank">
    <img src="https://img.shields.io/badge/🚀_Dùng_thử_trực_tiếp-Live_Web_Simulation-2563eb?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Live Demo"/>
  </a>
  <a href="docs/assets/demo.webp" target="_blank">
    <img src="https://img.shields.io/badge/🎞️_Xem_chuyển_động-True--Color_WebP-7c3aed?style=for-the-badge&logo=webm&logoColor=white" alt="WebP Animation"/>
  </a>
  <a href="docs/demo.html" target="_blank">
    <img src="https://img.shields.io/badge/💻_Mã_nguồn_Demo-docs%2Fdemo.html-10b981?style=for-the-badge&logo=html5&logoColor=white" alt="HTML Source"/>
  </a>
</p>

<p align="center">
  <em>🎮 <b>Quy trình tối ưu hóa lộ trình thực tế:</b> Du khách nhập ngân sách & sở thích &rarr; PADCS giải bài toán TOPTW đa ràng buộc &rarr; Xuất lịch trình du lịch từng giờ tối ưu. Nhấp vào ảnh hoặc nút bấm bên trên để mở bản chạy thử trực tiếp trên trình duyệt.</em>
</p>

<details>
<summary><b>🎞️ Nhấp vào đây để xem video ảnh động mô phỏng (Animation) ngay trên trang</b></summary>
<br/>
<p align="center">
  <img src="docs/assets/demo.gif" alt="PADCS Tour Optimization Animation" width="100%"/>
</p>
</details>

---

## 📌 Overview

**PADCS** (*Personalized Adaptive Destructive-Constructive Search*) is a hybrid Memetic Algorithm designed for solving the **Team Orienteering Problem with Time Windows (TOPTW)** with personalized multi-category scoring and realistic budget constraints.

Developed as a graduation thesis project at the **Faculty of Information Technology, VNU University of Engineering and Technology (VNU-UET)**, PADCS optimizes single-day travel itineraries by balancing:
- **Personalized Category Scores**: User interest ratings across 6 categories (`history_culture`, `nature_parks`, `food_drink`, `shopping`, `entertainment`, `nightlife_wellness`) normalized to sum to 6.0.
- **Temporal Constraints**: Specific visit time windows $[O_i, C_i]$ per Point of Interest (POI) and hard return deadlines to the depot.
- **Budgetary Constraints**: Category-specific ticket and service prices derived from Hanoi tourism economic statistics.
- **Wait Time Penalization**: Idle waiting minimization to ensure seamless travel scheduling.

The system is packaged with a high-performance **FastAPI** backend and an extensive empirical evaluation suite.

---

## 🧬 Algorithm Flowchart (Memetic Algorithm for P-OPTW)

The complete optimization lifecycle of PADCS—combining global genetic exploration, adaptive variation, and aggressive destructive-constructive local search—is illustrated below:

<p align="center">
  <img src="docs/assets/algorithm_flow.svg" alt="Memetic Algorithm for P-OPTW - Core Lifecycle" width="100%"/>
</p>

<details>
<summary><b>🔍 View Interactive Mermaid Diagram Code</b></summary>

```mermaid
flowchart LR
    subgraph P1 ["1. Initialization"]
        direction TB
        Start((Start)) --> S1["<b>1. Population Init</b><br/>80% RCL + 20% Random<br/>(N = 100 individuals)"]
        S1 --> S2["<b>2. Evaluate & Sort</b><br/>Repair & Refill each<br/>Calc fitness → Sort ↓"]
    end

    subgraph P2 ["2. Genetic Reproduction"]
        direction TB
        S3["<b>3. Selection</b><br/>Tournament (K=3)<br/>Select 2 Parents"]
        S3 --> S4["<b>4. Crossover OX1</b><br/>Interior Crossover<br/>(Depot-safe principle)"]
        S4 --> S5["<b>5. Mutation</b><br/>Adaptive-Lite<br/>(2-opt / Swap / Insert)"]
    end

    subgraph P3 ["3. Destructive-Constructive Search"]
        direction TB
        S6["<b>6. Smart Repair</b><br/>Ruin: bypass<br/>lowest ER POIs"]
        S6 --> S7["<b>7. Greedy Refill</b><br/>Recreate: insert unvisited<br/>high-score POIs greedily"]
        S7 --> S8["<b>8. Evaluate Fitness</b><br/>Calculate fitness<br/>and add to offspring pool"]
        S8 --> Decision{"<b>Pool Full?</b>"}
    end

    subgraph P4 ["4. Replacement & Termination"]
        direction TB
        S9["<b>9. Merged Replacement</b><br/>Merge parents + offspring<br/>Filter duplicates (Diversity)"]
        S9 --> S10["<b>10. Elitism & Stagnation</b><br/>Keep N best unique individuals<br/>Update stagnation counter"]
        S10 --> S11["<b>11. Check Termination</b><br/>Generations ≥ 200 or<br/>Stagnation counter ≥ 25"]
        S11 --> Stop(((Stop)))
    end

    S2 --> S3
    S5 --> S6
    Decision -- "[Yes]" --> S9
    Decision -.->|"[No] Loop size N"| S3
    S11 -.->|"[Next Gen] New Loop"| S3

    classDef initStyle fill:#EBF3FB,stroke:#2B5C8F,stroke-width:2px,color:#1A365D;
    classDef gaStyle fill:#FEF3E6,stroke:#D97724,stroke-width:2px,color:#7C3A00;
    classDef lsStyle fill:#EDF7ED,stroke:#2E7D32,stroke-width:2px,color:#1B5E20;
    classDef repStyle fill:#FBEBF0,stroke:#A0395E,stroke-width:2px,color:#621B35;
    classDef termStyle fill:#FDE8E8,stroke:#C62828,stroke-width:2px,color:#7F0000;
    classDef terminal fill:#2B5C8F,stroke:#1A365D,stroke-width:2px,color:#FFFFFF;

    class S1,S2 initStyle;
    class S3,S4,S5 gaStyle;
    class S6,S7,S8 lsStyle;
    class S9,S10 repStyle;
    class S11 termStyle;
    class Start,Stop terminal;
```
</details>

### Key Algorithmic Stages

| Step | Component | Technical Mechanism |
|---|---|---|
| **1-2** | **Population Initialization & Sorting** | 80% initialized via Restricted Candidate List (RCL) insertion heuristic + 20% random shuffle. Each individual is immediately repaired, refilled, evaluated, and sorted by fitness. |
| **3** | **Tournament Selection** | $K=3$ tournament selection picks two distinct parent solutions with replacement. |
| **4** | **OX1 Crossover** | Order Crossover (OX1) applied exclusively to interior nodes `route[1:-1]` to uphold the **Depot-Safe principle** `[0, ..., 0]`. |
| **5** | **Adaptive-Lite Mutation** | 2-tier adaptive probability matrix dynamically tuning 2-opt, Swap, and Insertion operators based on generation progress and population telemetry (stagnation, diversity, failure rate). |
| **6-7** | **Destructive-Constructive Local Search** | **Smart Repair** (Ruin): selectively prunes POIs with the lowest Efficiency Ratio $\text{ER} = \frac{\text{Score}}{\Delta\text{Time}}$ until all constraints are satisfied.<br/>**Greedy Refill** (Recreate): greedily inserts unvisited POIs offering maximum marginal score gain. |
| **8** | **Offspring Evaluation** | Evaluates multi-penalty fitness and feasibility, appending offspring to the candidate pool until pool size equals $N$. |
| **9-10** | **Merged Replacement & Elitism** | $(\mu+\lambda)$ elitist replacement merging parents and offspring ($2N$), filtering duplicate routes via POI set hashing to maintain genetic diversity, and preserving the top $N$ unique solutions. |
| **11** | **Termination Check** | Stops when reaching maximum generations (200) or when search stagnates for $\ge 25$ consecutive generations. |

---

## 📊 Empirical Benchmarks

The algorithm was thoroughly evaluated on the standard Solomon TOPTW benchmark instances (single-vehicle $m=1$), comparing against the state-of-the-art **GVNS** (Labadie et al., 2012) and **Best Known Solutions (BKS)** across 30 independent runs per instance.

### 1. Benchmark Comparison vs Labadie et al. (2012) GVNS

| Instance | BKS | GVNS Best | GVNS Avg | GVNS Gap% | PADCS Best | PADCS Avg | PADCS Std | PADCS Gap% | Avg Time (s) |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **C101** | 320 | 320 | 320.0 | 0.0% | **320.0** | 320.00 | 0.00 | **0.00%** | 7.09s |
| **C201** | 870 | 850 | 850.0 | 2.3% | **870.0** | 870.00 | 0.00 | **0.00%** | 38.05s |
| **R101** | 198 | 197 | 197.0 | 0.5% | **198.0** | 198.00 | 0.00 | **0.00%** | 6.41s |
| **R201** | 797 | 765 | 775.6 | 2.7% | **797.0** | 793.63 | 1.56 | **0.42%** | 68.51s |
| **RC101**| 219 | 219 | 219.0 | 0.0% | **219.0** | 219.00 | 0.00 | **0.00%** | 4.16s |
| **RC201**| 795 | 778 | 784.0 | 1.4% | **795.0** | 793.70 | 3.10 | **0.16%** | 46.88s |

> ⭐ **Key Result**: PADCS successfully discovered the **Best Known Solution (BKS)** on **100% (6/6)** benchmark instances, outperforming GVNS on C201, R101, R201, and RC201.

### 2. Ablation Study: Contribution of Destructive-Constructive Search

| Variant | Normalized Score (%) | Normalized Std | Avg Generations | Gap vs Full PADCS |
|:---|:---:|:---:|:---:|:---:|
| **Full PADCS (Smart Repair + Greedy Refill)** | **99.90%** | **0.28** | **37.3** | *Baseline* |
| **No Smart Repair (Simple tail-drop repair)** | 99.53% | 0.79 | 41.0 | -0.37% |
| **No Local Search (Repair & Refill disabled)** | 92.30% | 7.95 | 44.3 | **-7.60%** |

The ablation experiment clearly confirms that the hybrid Destructive-Constructive local search is vital for solution quality, improving normalized score by **+7.60%** over pure genetic operators.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/hm4uc/PADCS.git
cd PADCS

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
# source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the API Server

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- **API Base URL**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`

---

## 🧪 Reproducing Experiments

All experimental scripts are fully reproducible. On Windows, ensure UTF-8 console output is enabled:

```powershell
cd src
$env:PYTHONIOENCODING="utf-8"

# 1. Generate extended dataset (category classification + prices)
py -m experiments.generate_extended_data

# 2. Run Benchmark vs Labadie (2012)
py -m experiments.exp1_benchmark

# 3. Run Personalization impact across 5 tourist profiles
py -m experiments.exp2_personalization

# 4. Run Budget constraint evaluation across 3 tiers
py -m experiments.exp3_budget_impact

# 5. Run Ablation study on repair/refill operators
py -m experiments.exp4_ablation_repair

# 6. Run Parameter sensitivity experiments
py -m experiments.exp5_sensitivity

# 7. Aggregate results and generate publication charts
py -m experiments.analyze_results
py -m experiments.plot_charts
```

---

## 🔌 API Reference

### `POST /api/optimize`

Solves and returns the optimal itinerary for the given user preferences.

#### Request Example

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

#### Response Example

```json
{
  "total_score": 320.0,
  "total_cost": 380000.0,
  "total_distance": 68.45,
  "total_duration": 485.0,
  "execution_time": 0.42,
  "itinerary": [
    {
      "node_id": 0,
      "name": "Depot",
      "category": "depot",
      "arrival_time": "08:00",
      "wait_time": 0.0,
      "service_start": "08:00",
      "leave_time": "08:00",
      "score": 0.0,
      "cost": 0.0,
      "distance_from_prev": 0.0
    },
    {
      "node_id": 5,
      "name": "Temple of Literature",
      "category": "history_culture",
      "arrival_time": "08:25",
      "wait_time": 5.0,
      "service_start": "08:30",
      "leave_time": "09:30",
      "score": 100.0,
      "cost": 50000.0,
      "distance_from_prev": 8.5
    }
  ]
}
```

---

## 📁 Repository Structure

```
PADCS/
├── ARCHITECTURE_DOCUMENTATION.md   # Detailed Vietnamese technical architecture
├── LICENSE                         # MIT License
├── README.md                       # Main academic & technical documentation
├── requirements.txt                # Python package dependencies
├── references/                     # Academic literature & benchmark papers
├── docs/                           # Documentation & Interactive Demos
│   ├── demo.html                   # Standalone interactive tour planner web simulation
│   └── assets/                     # Vector diagrams, animations & demo assets
└── src/
    ├── main.py                     # FastAPI application bootstrap & CORS
    ├── api/                        # Route definitions (/api/optimize)
    ├── core/                       # Global hyperparameters & penalties
    ├── data/                       # Solomon benchmark instances & extended CSVs
    ├── models/                     # Domain & Pydantic schemas (requests/responses)
    ├── services/
    │   ├── data_loader.py          # Cached instance loader
    │   └── algorithm/              # Core optimization engine
    │       ├── padcs_engine.py     # Main memetic evolution loop
    │       ├── initialization.py   # Randomized insertion heuristic & random init
    │       ├── fitness.py          # Feasibility check & multi-penalty fitness
    │       ├── response_builder.py # HH:MM timeline formatter
    │       └── operators/          # Depot-safe genetic & local search operators
    │           ├── crossover.py    # OX1 crossover
    │           ├── mutation.py     # 2-opt, Swap, Insertion mutation
    │           └── repair.py       # Smart Repair & Greedy Refill
    └── experiments/                # Scientific experimentation suite
        ├── benchmark_runner.py     # Batch execution framework
        ├── exp1_benchmark.py       # Labadie (2012) comparison
        ├── exp2_personalization.py # Interest profile evaluation
        ├── exp3_budget_impact.py   # Budget constraint evaluation
        ├── exp4_ablation_repair.py # Destructive-constructive ablation
        ├── exp5_sensitivity.py     # Parameter sensitivity analysis
        ├── analyze_results.py      # Statistical aggregation
        ├── plot_charts.py          # Publication-ready figures
        └── results/                # Empirical CSVs & chart artifacts
```

---

## 📜 Citation

If you use PADCS or reference this work in your research, please cite:

```bibtex
@mastersthesis{duc2026padcs,
  title     = {Personalized Adaptive Destructive-Constructive Search for the Team Orienteering Problem with Time Windows},
  author    = {Hoang Minh Duc},
  school    = {VNU University of Engineering and Technology},
  year      = {2026},
  address   = {Hanoi, Vietnam}
}
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Hoang Minh Duc**  
Faculty of Information Technology, VNU University of Engineering and Technology (VNU-UET)  
GitHub: [@hm4uc](https://github.com/hm4uc)
