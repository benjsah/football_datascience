# Football Data Science - Modular Framework

A modular Python framework for predicting final league table positions in football leagues using Monte Carlo simulations based on a bivariate Poisson model.

## Project Structure

```
football_datascience/
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   └── loader.py          # Load and preprocess data from various sources
│   ├── preprocessing/
│   │   ├── __init__.py
│   │   ├── statistics.py      # Calculate team statistics and efficiency metrics
│   │   └── utils.py           # Utility functions for data preparation
│   ├── modelling/
│   │   ├── __init__.py
│   │   ├── poisson.py         # Poisson distribution model for match simulation
│   │   └── monte_carlo.py     # Monte Carlo simulation engine
│   └── visualization/
│       ├── __init__.py
│       └── plots.py           # Plotting and visualization functions
├── notebooks/
│   ├── season_end_prediction.ipynb  # Original Bundesliga notebook
│   └── template_new_league.ipynb    # Template for analyzing new leagues
├── configs/
│   ├── bundesliga.yaml        # Bundesliga configuration
│   ├── template.yaml          # Template for new leagues
│   └── [other_league].yaml    # Other league configurations
├── data/
│   └── raw/                   # Raw data files
├── tests/
│   └── test_*.py             # Unit tests
└── README.md
```

## Quick Start

### 1. Analyzing a New League

1. **Create a configuration file** in `configs/your_league.yaml`:
   ```bash
   cp configs/template.yaml configs/your_league.yaml
   ```

2. **Edit the configuration**:
   - Set league name and details
   - Configure data sources and file paths
   - Map team names to standardized format
   - Set simulation parameters

3. **Prepare your data files**:
   - Place fixture data (all season matches) in `data/raw/`
   - Place match statistics (detailed results) in `data/raw/`
   - Ensure column names match your configuration

4. **Run the analysis**:
   - Copy the template notebook: `cp notebooks/template_new_league.ipynb notebooks/your_league.ipynb`
   - Update the config file path in the first cell
   - Execute the notebook

## Core Modules

### `src.data.loader`
Handles loading and preparing data from various sources:
- `load_fixture_csv()` - Load fixture data
- `load_match_statistics()` - Load match statistics
- `normalize_team_names()` - Standardize team names across datasets

### `src.preprocessing.statistics`
Calculates team performance metrics:
- `calculate_home_team_statistics()` - Home team stats
- `calculate_away_team_statistics()` - Away team stats
- `calculate_efficiency_metrics()` - Attacking/defensive efficiency
- `calculate_league_table()` - Current or simulated league standings

### `src.modelling.poisson`
Implements Poisson distribution model:
- `simulate_match()` - Simulate single match outcome
- `calculate_expected_goals()` - Expected goals calculation
- `get_match_result()` - Convert goals to match result

### `src.modelling.monte_carlo`
Runs Monte Carlo simulations:
- `monte_carlo_simulation()` - Run full season simulations
- `calculate_position_probabilities()` - Probability of final positions
- `get_team_final_position_stats()` - Statistics for team's final position

### `src.visualization.plots`
Creates visualizations:
- `plot_position_probabilities_heatmap()` - Position probability heatmap
- `plot_team_position_distribution()` - Single team distribution
- `plot_multiple_teams_distribution()` - Compare multiple teams

## Configuration Format

Configuration files use YAML format and specify:

```yaml
league:
  name: "League Name"
  country: "Country"
  matches_per_team: 34

data_sources:
  all_matches:
    filename: "path/to/fixtures.csv"
  match_statistics:
    filename: "path/to/statistics.csv"

columns:
  # Column mappings for your data format
  all_matches: {...}
  match_stats: {...}

team_name_mapping:
  # Map source names to standardized names
  "Team A": "Standardized Team A"
  ...

simulation:
  n_simulations: 1000
  random_seed: 42
```

See `configs/template.yaml` for a complete template.

## Data Requirements

### Fixture Data (all_matches)
Required columns:
- Home Team
- Away Team
- Result (can be null for future matches)
- Round Number

### Match Statistics (match_stats)
Required columns:
- Date
- Home Team
- Away Team
- Home Goals (FTHG)
- Away Goals (FTAG)
- Full Time Result (H/A/D)
- Home Shots (HS)
- Away Shots (AS)
- Home Shots on Target (HST)
- Away Shots on Target (AST)

## Modeling Approach

### The Poisson Model

The framework uses a bivariate Poisson distribution to model football match outcomes:

1. **Expected Goals Calculation**:
   ```
   E[home_goals] = avg_home_shots * home_attack_eff * (1 - away_defense_eff)
   E[away_goals] = avg_away_shots * away_attack_eff * (1 - home_defense_eff)
   ```

2. **Efficiency Metrics**:
   - Attacking Efficiency = Goals Scored / Shots Made
   - Defensive Efficiency = Goals Conceded / Shots Conceded

3. **Match Simulation**:
   - Goals are sampled from Poisson distribution with calculated lambda
   - Each remaining match is simulated independently

4. **Monte Carlo Simulation**:
   - Run N simulations of remaining season
   - Calculate final league table for each simulation
   - Compute probability distribution of final positions

## Usage Example

```python
import yaml
from src.data import load_fixture_csv, load_match_statistics, prepare_fixtures, prepare_match_statistics
from src.preprocessing import calculate_home_team_statistics, calculate_away_team_statistics, calculate_efficiency_metrics
from src.modelling import monte_carlo_simulation, calculate_position_probabilities
from src.visualization import plot_position_probabilities_heatmap

# Load configuration
with open("configs/bundesliga.yaml") as f:
    config = yaml.safe_load(f)

# Load and prepare data
fixtures = load_fixture_csv("data/raw/fixtures.csv")
fixtures = prepare_fixtures(fixtures, config)

statistics = load_match_statistics("data/raw/stats.csv")
statistics = prepare_match_statistics(statistics, config)

# Calculate statistics
home_stats = calculate_home_team_statistics(statistics)
away_stats = calculate_away_team_statistics(statistics)
home_stats, away_stats = calculate_efficiency_metrics(home_stats, away_stats)

# Run simulations
league_tables, full_results = monte_carlo_simulation(
    fixtures, statistics, home_stats, away_stats,
    n_simulations=1000
)

# Calculate probabilities
position_probs = calculate_position_probabilities(league_tables)

# Visualize results
plot_position_probabilities_heatmap(position_probs)
```

## Adding a New League

1. Copy template configuration:
   ```bash
   cp configs/template.yaml configs/my_league.yaml
   ```

2. Edit `configs/my_league.yaml`:
   - Update league information
   - Set correct column names for your data format
   - Add team name mappings

3. Place data files in `data/raw/`:
   - Fixture data file
   - Match statistics file

4. Create notebook from template:
   ```bash
   cp notebooks/template_new_league.ipynb notebooks/my_league_2025.ipynb
   ```

5. Update config path in notebook and run!

## Dependencies

- pandas
- numpy
- matplotlib
- seaborn
- pyyaml

Install with:
```bash
pip install pandas numpy matplotlib seaborn pyyaml
```

## Output

The framework generates:

1. **League Table Probabilities**: Heatmap showing probability of each team finishing in each position
2. **Team Statistics**: Expected final position, probability of top finishes
3. **Detailed Results**: Full simulation results for analysis
4. **Visualizations**: Multiple plot types for different analyses

## Notes

- The original `season_end_prediction.ipynb` remains unchanged for reference
- All new analysis can use the modular framework
- Configuration-driven design allows easy expansion to new leagues
- Monte Carlo approach provides robust probability estimates
- Random seed ensures reproducible results

## Future Enhancements

Possible improvements to the framework:
- Add rating-based models (e.g., Elo/Bradley-Terry)
- Include head-to-head records
- 3-way Poisson (correlation between goals)
- Injury probability factors
- Regression analysis of model predictions
- Support for multiple divisions

## License

This project is part of the football data science initiative.
