"""
Poisson model for match simulation.

This module implements a bivariate Poisson distribution model to simulate
football match outcomes based on team statistics and efficiency metrics.
"""

import numpy as np
import pandas as pd
from typing import Tuple


def calculate_expected_goals(
    home_team: str, away_team: str, home_stats: pd.DataFrame, away_stats: pd.DataFrame
) -> Tuple[float, float]:
    """
    Calculate expected goals for both teams using efficiency metrics.

    Formula:
    expected_goals = shots_made * attacking_efficiency * (1 - opponent_defense_efficiency)

    Args:
        home_team: Name of home team
        away_team: Name of away team
        home_stats: DataFrame with home team statistics
        away_stats: DataFrame with away team statistics

    Returns:
        Tuple of (expected_home_goals, expected_away_goals)
    """
    # Get team statistics
    home_team_stats = home_stats.loc[home_team]
    away_team_stats = away_stats.loc[away_team]

    # Get efficiency metrics
    home_attack_eff = home_stats.loc[home_team, "home_attack_eff"]
    home_defense_eff = home_stats.loc[home_team, "home_defense_eff"]
    away_attack_eff = away_stats.loc[away_team, "away_attack_eff"]
    away_defense_eff = away_stats.loc[away_team, "away_defense_eff"]

    # Calculate expected goals
    expected_home_goals = (
        home_team_stats["avg_home_shots_made"] * home_attack_eff * (away_defense_eff)
    )

    expected_away_goals = (
        away_team_stats["avg_away_shots_made"] * away_attack_eff * (home_defense_eff)
    )

    return expected_home_goals, expected_away_goals


def simulate_match(
    home_team: str, away_team: str, home_stats: pd.DataFrame, away_stats: pd.DataFrame
) -> Tuple[int, int]:
    """
    Simulate a single football match using Poisson distribution.

    The number of goals scored by each team is drawn from a Poisson distribution
    with lambda parameter equal to the expected goals calculated from team statistics.

    Args:
        home_team: Name of home team
        away_team: Name of away team
        home_stats: DataFrame with home team statistics
        away_stats: DataFrame with away team statistics

    Returns:
        Tuple of (home_goals, away_goals)
    """
    # Calculate expected goals
    expected_home_goals, expected_away_goals = calculate_expected_goals(
        home_team, away_team, home_stats, away_stats
    )

    # Bound expected goals to avoid numerical issues
    expected_home_goals = max(0.1, min(expected_home_goals, 20))
    expected_away_goals = max(0.1, min(expected_away_goals, 20))

    # Sample goals from Poisson distribution
    home_goals = np.random.poisson(expected_home_goals)
    away_goals = np.random.poisson(expected_away_goals)

    return int(home_goals), int(away_goals)


def get_match_result(home_goals: int, away_goals: int) -> str:
    """
    Determine match result from goal counts.

    Args:
        home_goals: Number of home team goals
        away_goals: Number of away team goals

    Returns:
        Result code: "H" (home win), "A" (away win), or "D" (draw)
    """
    if home_goals > away_goals:
        return "H"
    elif away_goals > home_goals:
        return "A"
    else:
        return "D"
