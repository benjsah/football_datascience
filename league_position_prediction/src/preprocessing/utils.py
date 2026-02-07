"""
Utility functions for data preprocessing.
"""

import pandas as pd
from typing import Tuple


def split_result_column(
    df: pd.DataFrame, result_col: str = "Result"
) -> Tuple[pd.DataFrame, list]:
    """
    Split result string (e.g., "2-1") into home and away goals.

    Args:
        df: DataFrame containing result column
        result_col: Name of the result column

    Returns:
        Tuple of (updated DataFrame with Home Goals and Away Goals columns,
                  list of rows with invalid format)
    """
    df = df.copy()
    invalid_rows = []

    def parse_result(result):
        if pd.isna(result):
            return None, None
        try:
            parts = str(result).split("-")
            if len(parts) != 2:
                return None, None
            return int(parts[0].strip()), int(parts[1].strip())
        except (ValueError, AttributeError):
            return None, None

    home_goals = []
    away_goals = []

    for idx, result in enumerate(df[result_col]):
        home, away = parse_result(result)
        if home is None or away is None:
            invalid_rows.append(idx)
        home_goals.append(home)
        away_goals.append(away)

    df["Home Goals"] = home_goals
    df["Away Goals"] = away_goals

    return df, invalid_rows


def create_played_matches_dataframe(stats_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create DataFrame with only played matches (those with results).

    Args:
        stats_df: Statistics DataFrame with match results

    Returns:
        DataFrame with played matches only, relevant columns selected
    """
    df = stats_df.copy()

    # Drop unnecessary columns
    columns_to_keep = ["Home Team", "Away Team", "Home Goals", "Away Goals", "Result"]
    columns_to_keep = [col for col in columns_to_keep if col in df.columns]

    df = df[columns_to_keep]

    return df


def create_remaining_matches_dataframe(fixtures_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create DataFrame with only remaining matches (those without results).

    Args:
        fixtures_df: Fixtures DataFrame

    Returns:
        DataFrame with remaining matches only
    """
    df = fixtures_df.copy()

    # Filter for matches without results
    remaining = df[df["Result"].isnull()].reset_index(drop=True)

    # Drop unnecessary columns
    columns_to_keep = ["Home Team", "Away Team"]
    remaining = remaining[columns_to_keep]

    return remaining
