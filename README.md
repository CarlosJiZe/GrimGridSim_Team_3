# GrimGridSim_Team_3

A comprehensive energy management simulation system for solar-powered microgrids with battery storage. This digital twin simulates real-world energy dynamics, financial performance, and reliability metrics for residential or commercial solar installations.

**Project:** Phase 1 - Simulation & Data Generation  
**Course:** COM 139 - Simulation & Visualization  
**Institution:** Universidad Panamericana, Guadalajara  
**Team:** Team 3

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Output Files](#-output-files)
- [Advanced Usage](#-advanced-usage)
- [Troubleshooting](#-troubleshooting)
- [Future Phases](#-future-phases)

---

## ✨ Features

### Core Simulation
- **Real-time energy flow modeling**: Solar generation, battery storage, load consumption, and grid interaction
- **Multiple energy management strategies**: LOAD_PRIORITY, CHARGE_PRIORITY, PRODUCE_PRIORITY
- **Seasonal variations**: Realistic cloud coverage and daylight patterns for spring, summer, fall, and winter
- **Reliability simulation**: Inverter failures with configurable rates and durations
- **Financial modeling**: Import costs, export revenues, and ROI calculations

### Advanced Features
- **Strategy comparison tool**: Automatically compare all three energy management strategies
- **Seasonal comparison**: Evaluate system performance across all four seasons
- **Scalable system sizing**: Configure multiple batteries, solar arrays, and inverters
- **Reproducible results**: Optional random seed for consistent testing
- **Comprehensive data export**: CSV, JSON, and text report formats

---

## 🚀 Quick Start

### For Impatient Users (3 Steps)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd greengrid-simulation

# 2. Run the simulation
python3 main.py

# 3. View results
cat results/answers.txt
```

That's it! The simulation will run with default settings and generate results in the `results/` folder.

---

## 💻 Installation

### Prerequisites

- **Python 3.8 or higher** (3.9+ recommended)
- No external libraries required! Uses only Python standard library

### Verify Python Version

```bash
python3 --version
# Should show Python 3.8.0 or higher
```

### Clone the Repository

```bash
git clone <your-repo-url>
cd greengrid-simulation
```

### Verify Installation

```bash
python3 main.py
# If you see the GreenGrid header, you're ready to go!
```

---

## ⚙️ Configuration

### Configuration Files

The simulation uses `config.json` in the `simulator` file for all settings. A template with detailed explanations is provided in `config_template.json`.

### Quick Configuration

**Option 1: Use the provided config.json** (recommended for first run)
```bash
# No action needed - default config is already included
python3 main.py
```

**Option 2: Customize your configuration**
```bash
# Copy the template
cp config_template.json config.json

# Edit with your preferred editor
nano config.json
# or
vim config.json
```

### Key Configuration Parameters

#### Simulation Settings
```json
{
  "simulation": {
    "duration_days": 30,           // Simulation length (30 days = 1 month)
    "time_step_minutes": 60,       // Time resolution (15, 30, or 60)
    "start_date": "2024-06-01",    // Starting date (affects sun angle)
    "season": "summer",            // Season: spring, summer, fall, winter
    "random_seed": 519425893       // For reproducible results (or null)
  }
}
```

#### System Components
```json
{
  "battery": {
    "unit_capacity_kwh": 13.5,     // Capacity per battery (13.5 = Tesla Powerwall)
    "count": 1,                    // Number of batteries
    "efficiency": 0.9,             // Round-trip efficiency (90%)
    "min_soc": 0.05               // Minimum charge level (5%)
  },
  "solar": {
    "unit_peak_power_kw": 5.0,     // Peak power per array (5 kW)
    "count": 1                     // Number of solar arrays
  },
  "inverter": {
    "unit_max_output_kw": 4.0,     // Max output per inverter
    "count": 1,                    // Number of inverters
    "failure_rate": 0.005          // Daily failure probability (0.5%)
  }
}
```

#### Energy Management
```json
{
  "energy_management": {
    "strategy": "LOAD_PRIORITY"    // LOAD_PRIORITY, CHARGE_PRIORITY, or PRODUCE_PRIORITY
  }
}
```

### Energy Management Strategies Explained

| Strategy | Priority Order | Best For |
|----------|---------------|----------|
| **LOAD_PRIORITY** | 1. Load → 2. Battery → 3. Grid Export | Maximizing self-consumption |
| **CHARGE_PRIORITY** | 1. Battery → 2. Load → 3. Grid Export | Backup power / time-of-use rates |
| **PRODUCE_PRIORITY** | 1. Grid Export → 2. Load → 3. Battery | Revenue maximization |

### Example Configurations

#### Small Residential (Current Default)
```json
{
  "battery": {"count": 1, "unit_capacity_kwh": 13.5},
  "solar": {"count": 1, "unit_peak_power_kw": 5.0},
  "inverter": {"count": 1, "unit_max_output_kw": 4.0}
}
```

#### Medium Residential
```json
{
  "battery": {"count": 2, "unit_capacity_kwh": 13.5},
  "solar": {"count": 3, "unit_peak_power_kw": 5.0},
  "inverter": {"count": 2, "unit_max_output_kw": 4.0}
}
```

#### Large Residential / Small Commercial
```json
{
  "battery": {"count": 4, "unit_capacity_kwh": 13.5},
  "solar": {"count": 3, "unit_peak_power_kw": 10.0},
  "inverter": {"count": 2, "unit_max_output_kw": 10.0}
}
```

---

## 🎯 Usage

### Basic Simulation

Run a single simulation with your current configuration:

```bash
python3 main.py
```

**What happens:**
1. Loads configuration from `config.json`
2. Displays system parameters
3. Prompts for confirmation
4. Runs the simulation
5. Displays results summary
6. Saves detailed data to `results/` folder

**Expected Output:**
```
======================================================================
   ___                  ___     _     _   ___ _          
  / __|_ _ ___ ___ _ _ / __|_ _(_)__| | / __(_)_ __     
 | (_ | '_/ -_) -_) ' \ (_ | '_| / _` | \__ \ | '  \    
  \___|_| \___\___|_||_\___|_| |_\__,_| |___/_|_|_|_|   

          Digital Twin Simulation - Phase 1
======================================================================

📋 SIMULATION CONFIGURATION:
  Duration: 30 days
  Season: summer
  Strategy: LOAD_PRIORITY
  ...

▶ Press ENTER to start simulation (or Ctrl+C to cancel):
```

### Strategy & Season Comparison

Compare all strategies and seasons in one run:

```bash
python3 compare_strategies.py
```

**What happens:**
1. Runs 7 total simulations:
   - 3 strategy comparisons (LOAD, CHARGE, PRODUCE)
   - 4 seasonal comparisons (spring, summer, fall, winter)
2. Uses the same random seed for fair comparison
3. Generates comprehensive comparison report
4. Saves to `results/comparison_report_TIMESTAMP.txt`

**Duration:** Approximately 3-5 minutes on modern hardware

---

## 📁 Project Structure

```
greengrid-simulation/
│
├── main.py                      # Main simulation entry point
├── compare_strategies.py        # Strategy/season comparison tool
├── config.json                  # Active configuration (edit this)
├── config_template.json         # Configuration template with help
│
├── src/                         # Source code modules
│   ├── Simulation.py            # Main simulation engine
│   ├── DataLogger.py            # Data export and logging
│   ├── SolarPanel.py            # Solar generation model
│   ├── Battery.py               # Battery storage model
│   ├── Inverter.py              # Inverter with failure simulation
│   ├── EnergyManager.py         # Energy management strategies
│   └── ...                      # Other components
│
├── results/                     # Generated output files (created on first run)
│   ├── hourly_data_TIMESTAMP.csv       # Detailed time-series data
│   ├── summary_TIMESTAMP.json          # JSON summary
│   ├── answers_TIMESTAMP.txt           # Project Q&A answers
│   └── comparison_report_TIMESTAMP.txt # Strategy comparison report
│
└── README.md                    # This file
```

---

## 📊 Output Files

After running the simulation, you'll find these files in the `results/` folder:

### 1. `hourly_data_YYYYMMDD_HHMMSS.csv`
Detailed time-series data for every simulation hour.

**Columns:**
- `timestamp`: Date and time
- `solar_generated_kw`: Solar power output (kW)
- `load_consumed_kw`: Power consumed by load (kW)
- `battery_soc_percent`: Battery charge level (%)
- `grid_import_kw`, `grid_export_kw`: Grid interaction (kW)
- `cloud_coverage`, `inverter_operational`: Environmental & reliability data
- And more...

**Use case:** Time-series analysis, detailed debugging, visualization (Phase 2)

### 2. `summary_YYYYMMDD_HHMMSS.json`
High-level summary of simulation results in JSON format.

**Contains:**
```json
{
  "summary": {
    "total_solar_generated_kwh": 1234.56,
    "total_load_consumed_kwh": 987.65,
    "self_sufficiency_percent": 65.4,
    ...
  },
  "financial": {
    "total_import_cost": 12.34,
    "total_export_revenue": 23.45,
    "net_cost": -11.11,
    ...
  },
  "battery": { ... },
  "reliability": { ... }
}
```

**Use case:** Quick overview, API integration, dashboard data

### 3. `answers_YYYYMMDD_HHMMSS.txt`
Comprehensive report answering all project questions.

**Sections:**
- System configuration summary
- Financial analysis
- Performance metrics
- Strategy evaluation
- Recommendations

**Use case:** Project documentation, presentations, reports

### 4. `comparison_report_YYYYMMDD_HHMMSS.txt`
Generated by `compare_strategies.py` - compares strategies and seasons.

**Contains:**
- Strategy comparison table
- Best/worst strategy analysis
- Seasonal performance comparison
- System sizing recommendations

**Use case:** Strategy selection, seasonal planning, system optimization

---

## 🔧 Advanced Usage

### Reproducible Simulations

To get identical results every time (useful for debugging or comparisons):

1. Set a random seed in `config.json`:
```json
{
  "simulation": {
    "random_seed": 519425893
  }
}
```

2. Run the simulation - results will be identical every time

**When to use:**
- ✅ Comparing different configurations
- ✅ Debugging issues
- ✅ Reproducible research
- ❌ General testing (use `null` for variety)

### Customizing Load Patterns

Edit the load profile in `config.json`:

```json
{
  "load": {
    "base_load_kw": 0.5,          // 24/7 background load (fridge, router)
    "peak_hours_max_kw": 3.0,     // Evening peak load (cooking, AC)
    "peak_hours_start": 18,       // 6:00 PM using the 24hrs format
    "peak_hours_end": 21          // 9:00 PM using the 24hrs format
  }
}
```

**Tip:** Model your actual home by:
1. Check your monthly kWh consumption
2. Divide by ~720 hours/month for average kW
3. Set `base_load_kw` to 60-70% of average
4. Set `peak_hours_max_kw` to 2-3x average

### Fine-tuning Time Resolution

More detailed analysis? Change the time step:

```json
{
  "simulation": {
    "time_step_minutes": 15    // 15, 30, or 60 minutes
  }
}
```

**Trade-offs:**
- 15 minutes = More detailed (4x data) but slower
- 60 minutes = Faster, less detailed (default)

### Grid Configuration

Customize grid interaction:

```json
{
  "grid": {
    "import_cost_per_kwh": 0.0075,    // $0.0075/kWh = 0.75 USD cents 
    "export_revenue_per_kwh": 0.009,  // $0.009/kWh = 0.9 USD cents
    "export_limit_kw": 20.0           // Maximum export capacity
  }
}
```

**Real-world mapping:**
- US typical: import ~$0.12/kWh, export ~$0.03/kWh
- Mexico CFE: import ~MXN 2.5/kWh (~$0.15), limited export programs
- Adjust to match your local utility rates

---

## 🐛 Troubleshooting

### Common Issues

#### `FileNotFoundError: config.json`

**Problem:** Configuration file is missing

**Solution:**
```bash
# Copy the template
cp config_template.json config.json
```

#### `ModuleNotFoundError: No module named 'src'`

**Problem:** Python can't find the source modules

**Solutions:**
1. Make sure you're in the project root directory:
```bash
cd greengrid-simulation
python3 main.py
```

2. Verify the `src/` folder exists and contains Python files

#### Simulation runs but no results folder

**Problem:** Permissions issue or disk space

**Solution:**
```bash
# Manually create results folder
mkdir -p results

# Check disk space
df -h .
```

#### Very low self-sufficiency (<20%)

**Problem:** System is undersized for the load

**Solutions:**
1. Increase battery capacity:
```json
{"battery": {"count": 2}}  // Double the battery
```

2. Increase solar generation:
```json
{"solar": {"count": 2}}    // Double the panels
```

3. Or reduce load:
```json
{
  "load": {
    "base_load_kw": 0.3,      // Reduce from 0.5
    "peak_hours_max_kw": 2.0  // Reduce from 3.0
  }
}
```

#### Results vary wildly between runs

**Problem:** Random seed is not set

**Solution:**
```json
{
  "simulation": {
    "random_seed": 123456789   // Set any integer
  }
}
```

---

## 🔮 Future Phases

This is **Phase 1** of a three-phase project:

### Phase 2: Visualization (Next)
- Interactive dashboards with real-time data
- Time-series plots (energy flow, battery state, costs)
- Geographical heat maps
- Strategy comparison charts
- 3D visualizations

### Phase 3: Machine Learning
- Predictive models for energy generation
- Load forecasting algorithms
- Anomaly detection for system failures
- Optimization recommendations
- Reinforcement learning for strategy selection


---

## 📝 Configuration Tips

### For Maximum Self-Sufficiency
```json
{
  "battery": {"count": 3, "unit_capacity_kwh": 13.5},  // 40.5 kWh total
  "solar": {"count": 4, "unit_peak_power_kw": 5.0},    // 20 kW peak
  "energy_management": {"strategy": "LOAD_PRIORITY"}
}
```

### For Maximum Export Revenue
```json
{
  "solar": {"count": 5, "unit_peak_power_kw": 5.0},     // 25 kW peak
  "battery": {"count": 1, "unit_capacity_kwh": 13.5},   // Minimal battery
  "energy_management": {"strategy": "PRODUCE_PRIORITY"}
}
```

### For Backup Power Resilience
```json
{
  "battery": {"count": 4, "unit_capacity_kwh": 13.5},   // 54 kWh total
  "battery": {"min_soc": 0.20},                         // Keep 20% reserve
  "energy_management": {"strategy": "CHARGE_PRIORITY"}
}
```

### For Testing Edge Cases
```json
{
  "simulation": {"duration_days": 90},               // Full season
  "inverter": {"failure_rate": 0.02},                // 2% failure (high)
  "simulation": {"time_step_minutes": 15},           // High resolution
  "load": {"peak_hours_max_kw": 5.0}                 // High demand
}
```

---

## 📚 Additional Resources

### Understanding the Metrics

**Self-Sufficiency (%)**: Percentage of load met by solar + battery (without grid import)
- 100% = Fully off-grid capable
- 50-70% = Typical residential solar system
- <30% = Undersized system

**Net Cost ($)**: Import cost minus export revenue
- Negative = System is profitable (exporting more than importing)
- Positive = System costs money (importing more than exporting)
- Goal: Minimize this value

**Average Battery SoC (%)**: Average battery charge level
- 70-80% = Healthy, well-sized system
- 40-60% = Battery could be larger
- >90% = Battery may be oversized

**Curtailed Energy (kWh)**: Wasted solar energy that couldn't be used
- Reasons: Battery full, load satisfied, export limit reached
- High curtailment = Consider larger battery or increasing load

---

## 🤝 Contributing

This is an academic project, but suggestions are welcome!

**Found a bug?**
1. Note the exact error message
2. Share your `config.json` file
3. Describe steps to reproduce

**Have an improvement idea?**
1. Describe the feature
2. Explain the use case
3. Suggest implementation approach

---

## 📄 License

Academic project for Simulation & Visualization  
Universidad Panamericana, Guadalajara  
Team 3

---

## 🎓 Authors

Team 3 - GreenGrid Project  
Course: Simulation & Visualization  
Institution: Universidad Panamericana, Guadalajara
Carlos Jimenez Zepeda
Andres Gonzalez Gomez
Martin Garcia Torres

---

## 🙋 Need Help?

1. **Check this README** - Most questions are answered here
2. **Review `config_template.json`** - Has detailed parameter explanations
3. **Run with default config** - Use provided `config.json` for guaranteed working setup
4. **Check the Troubleshooting section** - Common issues and solutions

**Happy Simulating! 🌱⚡**