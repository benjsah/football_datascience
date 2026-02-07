# Quick Start Guide

## Overview

This framework allows you to analyze any football league's season predictions using Monte Carlo simulations. The modular design makes it easy to work with different leagues by simply swapping configuration files.

## 5-Minute Setup for a New League

### Step 1: Create Configuration File
```bash
cp configs/template.yaml configs/your_league.yaml
```

### Step 2: Edit Configuration

Open `configs/your_league.yaml` and update:

```yaml
league:
  name: "Your League"
  country: "Country"

data_sources:
  all_matches:
    filename: "your_fixtures_file.csv"  # All season matches
  match_statistics:
    filename: "your_stats_file.csv"     # Played matches with stats

columns:
  all_matches:
    home_team: "Home Team"              # Your column name
    away_team: "Away Team"
    result: "Result"
    round_number: "Round"
  match_stats:
    home_team: "HTName"                 # Your column names  
    away_team: "ATName"
    home_goals: "HG"
    away_goals: "AG"
    # ... other columns

team_name_mapping:                       # Standardize team names
  "Team A Source": "Team A Standard"
  "Team B Source": "Team B Standard"
```

### Step 3: Prepare Data

Place your data files in `data/raw/`:
- Fixture file with all season matches (including unplayed)
- Statistics file with played matches and detailed stats

### Step 4: Run Analysis

Copy and run the template notebook:

```bash
cp notebooks/template_new_league.ipynb notebooks/your_league_analysis.ipynb
```

Update the first cell:
```python
config_file = "../configs/your_league.yaml"
```

Then execute all cells!

## What You Get

The analysis produces:

1. **Probability Heatmap** - Each team's chance of finishing in each position
2. **Team Statistics** - Expected finish position, top 4 probability, etc.
3. **League Table** - Current standings and simulated final table
4. **Visualizations** - Multiple plot types for different analyses

## File Structure

```
football_datascience/
├── src/                          # Core modules
│   ├── data/loader.py
│   ├── preprocessing/statistics.py
│   ├── modelling/monte_carlo.py
│   └── visualization/plots.py
├── notebooks/
│   ├── season_end_prediction.ipynb    # Original (unchanged)
│   ├── template_new_league.ipynb      # Use this template
│   └── your_league.ipynb              # Your analysis
├── configs/
│   ├── bundesliga.yaml                # Example
│   ├── template.yaml                  # Copy this
│   └── your_league.yaml               # Your config
└── data/raw/                          # Your data files
```

## Module Overview

### Data Loading (`src.data.loader`)
- Loads fixtures and match statistics
- Normalizes team names across datasets
- Prepares data for analysis

### Preprocessing (`src.preprocessing`)
- Calculates team statistics (goals, shots, etc.)
- Computes efficiency metrics
- Generates league tables

### Modelling (`src.modelling`)
- **Poisson**: Simulates individual matches
- **Monte Carlo**: Runs 1000 season simulations
- Calculates position probabilities

### Visualization (`src.visualization`)
- Heatmaps of final positions
- Distribution plots
- Comparative analysis plots

## Tips

1. **Team Name Mapping**: This is crucial! Ensure names match between fixture and statistics files
2. **Column Names**: Carefully check your data format and update column names in config
3. **Data Quality**: Remove null values and duplicate matches before analyzing
4. **Simulations**: More simulations = more accurate probabilities but longer runtime

## Troubleshooting

**Problem**: Team names don't match
**Solution**: Update `team_name_mapping` in your config file

**Problem**: KeyError with column names
**Solution**: Check `columns` section in config matches your actual data

**Problem**: Slow execution
**Solution**: Reduce `n_simulations` in config (default 1000) for testing

## Example Configuration Sections

### Bundesliga (Germany)
```yaml
team_name_mapping:
  "Bayern Munich": "FC Bayern München"
  "Dortmund": "Borussia Dortmund"
  "Leverkusen": "Bayer 04 Leverkusen"
```

### Serie A (Italy)
```yaml
team_name_mapping:
  "Napoli": "SSC Napoli"
  "Roma": "AS Roma"
  "Milano": "AC Milan"
```

## Next Steps

1. Check `FRAMEWORK_README.md` for detailed documentation
2. Review the original `season_end_prediction.ipynb` for methodology
3. Examine `src/` modules for function documentation
4. Run with different simulation counts to understand sensitivity

## Questions?

Refer to:
- `FRAMEWORK_README.md` - Complete framework documentation
- Individual module docstrings - Function-level documentation
- `template_new_league.ipynb` - Working example with explanations
