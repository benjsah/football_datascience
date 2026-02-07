"""
Data loading module for football league data from various sources.

This module provides functions to load and preprocess match data from:
- fixture-download.com (fixture data)
- football-data.co.uk (detailed match statistics)
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Tuple


def load_fixture_csv(filepath: str) -> pd.DataFrame:
    """
    Load fixture data from CSV file.

    Expected columns: "Date", "Location", "Match Number", "Round Number",
                      "Home Team", "Away Team", "Result"

    Args:
        filepath: Path to the CSV file

    Returns:
        DataFrame with fixture data
    """
    df = pd.read_csv(filepath)
    return df


def load_match_statistics(filepath: str) -> pd.DataFrame:
    """
    Load match statistics from CSV file (football-data.co.uk format).

    Expected columns: "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR",
                      "HS", "AS", "HST", "AST", etc.

    Args:
        filepath: Path to the CSV file

    Returns:
        DataFrame with match statistics
    """
    df = pd.read_csv(filepath)
    return df


def normalize_team_names(
    df: pd.DataFrame,
    team_mapping: Dict[str, str],
    home_team_col: str = "Home Team",
    away_team_col: str = "Away Team",
) -> pd.DataFrame:
    """
    Normalize team names in a DataFrame using a mapping dictionary.

    Args:
        df: Input DataFrame
        team_mapping: Dictionary mapping source names to target names
        home_team_col: Name of home team column
        away_team_col: Name of away team column

    Returns:
        DataFrame with normalized team names
    """
    df = df.copy()

    if home_team_col in df.columns:
        df[home_team_col] = df[home_team_col].replace(team_mapping)
    if away_team_col in df.columns:
        df[away_team_col] = df[away_team_col].replace(team_mapping)

    return df


def prepare_match_statistics(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """
    Prepare match statistics DataFrame for analysis.

    - Selects only necessary columns
    - Renames columns for consistency
    - Normalizes team names
    - Converts result column to appropriate format

    Args:
        df: Input match statistics DataFrame
        config: Configuration dictionary with column mappings and team name mappings

    Returns:
        Prepared DataFrame with standardized column names
    """
    df = df.copy()

    cols_config = config["columns"]["match_stats"]

    # Select and rename columns
    columns_to_select = {
        cols_config["date"]: "Date",
        cols_config["home_team"]: "Home Team",
        cols_config["away_team"]: "Away Team",
        cols_config["home_goals"]: "Home Goals",
        cols_config["away_goals"]: "Away Goals",
        cols_config["result"]: "Result",
        cols_config["home_shots"]: "Home Shots",
        cols_config["away_shots"]: "Away Shots",
        cols_config["home_shots_on_target"]: "Home Shots on Target",
        cols_config["away_shots_on_target"]: "Away Shots on Target",
    }

    # Only select columns that exist in the DataFrame
    columns_to_select = {k: v for k, v in columns_to_select.items() if k in df.columns}

    df = df[list(columns_to_select.keys())].rename(columns=columns_to_select)

    # Normalize team names
    df = normalize_team_names(df, config["team_name_mapping"])

    return df


def prepare_fixtures(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """
    Prepare fixtures DataFrame for analysis.

    Args:
        df: Input fixtures DataFrame
        config: Configuration dictionary

    Returns:
        Prepared DataFrame with standardized column names
    """
    df = df.copy()

    cols_config = config["columns"]["all_matches"]

    # Select and rename columns
    columns_to_select = {
        cols_config["home_team"]: "Home Team",
        cols_config["away_team"]: "Away Team",
        cols_config["result"]: "Result",
        cols_config["round_number"]: "Round Number",
    }

    # Only select columns that exist
    columns_to_select = {k: v for k, v in columns_to_select.items() if k in df.columns}

    df = df[list(columns_to_select.keys())].rename(columns=columns_to_select)

    # Normalize team names
    df = normalize_team_names(df, config["team_name_mapping"])

    return df


def load_and_process_league_data(
    config: Dict[str, Any], data_dir: str = "data/raw"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load and process all league data from configured sources.

    Args:
        config: Configuration dictionary
        data_dir: Base directory containing raw data files

    Returns:
        Tuple of (fixtures DataFrame, statistics DataFrame)
    """
    data_path = Path(data_dir)

    # Load fixtures
    fixtures_file = data_path / config["data_sources"]["all_matches"]["filename"]
    fixtures = load_fixture_csv(str(fixtures_file))
    fixtures = prepare_fixtures(fixtures, config)

    # Load match statistics
    stats_file = data_path / config["data_sources"]["match_statistics"]["filename"]
    statistics = load_match_statistics(str(stats_file))
    statistics = prepare_match_statistics(statistics, config)

    return fixtures, statistics
