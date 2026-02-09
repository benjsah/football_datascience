"""
Statistics calculation module for team performance metrics.

This module provides functions to calculate team statistics from match data,
including goals, shots, and efficiency metrics needed for the Poisson model.
"""

import pandas as pd
import numpy as np
from typing import Tuple


def calculate_home_team_statistics(stats_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate home team statistics from match data.

    Returns average goals scored and conceded as home team,
    as well as average shots made and conceded.

    Args:
        stats_df: DataFrame with match statistics
                  Expected columns: "Home Team", "Home Goals", "Away Goals",
                                   "Home Shots", "Away Shots"

    Returns:
        DataFrame indexed by team with columns:
        - avg_home_goals_scored
        - avg_home_goals_conceded
        - avg_home_shots_made
        - avg_home_shots_conceded
    """
    home_stats = stats_df.groupby("Home Team").agg(
        {
            "Home Goals": "mean",
            "Away Goals": "mean",
            "Home Shots": "mean",
            "Away Shots": "mean",
        }
    )

    home_stats.columns = [
        "avg_home_goals_scored",
        "avg_home_goals_conceded",
        "avg_home_shots_made",
        "avg_home_shots_conceded",
    ]

    return home_stats


def calculate_away_team_statistics(stats_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate away team statistics from match data.

    Returns average goals scored and conceded as away team,
    as well as average shots made and conceded.

    Args:
        stats_df: DataFrame with match statistics
                  Expected columns: "Away Team", "Home Goals", "Away Goals",
                                   "Home Shots", "Away Shots"

    Returns:
        DataFrame indexed by team with columns:
        - avg_away_goals_scored
        - avg_away_goals_conceded
        - avg_away_shots_made
        - avg_away_shots_conceded
    """
    away_stats = stats_df.groupby("Away Team").agg(
        {
            "Away Goals": "mean",
            "Home Goals": "mean",
            "Away Shots": "mean",
            "Home Shots": "mean",
        }
    )

    away_stats.columns = [
        "avg_away_goals_scored",
        "avg_away_goals_conceded",
        "avg_away_shots_made",
        "avg_away_shots_conceded",
    ]

    return away_stats


def calculate_efficiency_metrics(
    home_stats: pd.DataFrame, away_stats: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calculate attacking and defensive efficiency metrics for teams.

    Efficiency is calculated as:
    - Chance creation efficiency = shots made / league average shots made
    - Chance suppression efficiency = shots conceded / league average shots conceded
    - Attacking efficiency = goals scored / shots made
    - Defensive efficiency = goals conceded / shots conceded

    Args:
        home_stats: Home team statistics DataFrame
        away_stats: Away team statistics DataFrame

    Returns:
        Tuple of (home_stats with efficiency metrics, away_stats with efficiency metrics)
    """
    home_stats = home_stats.copy()
    away_stats = away_stats.copy()

    # Calculate league averages for shots made and conceded
    league_avg_home_shots_made = home_stats["avg_home_shots_made"].mean()
    league_avg_home_shots_conceded = home_stats["avg_home_shots_conceded"].mean()
    league_avg_away_shots_made = away_stats["avg_away_shots_made"].mean()
    league_avg_away_shots_conceded = away_stats["avg_away_shots_conceded"].mean()

    # Calculate chance creation and suppression efficiency for home and away teams compared to league averages
    # Avoid division by zero
    home_stats["home_chance_creation_eff"] = (
        home_stats["avg_home_shots_made"] / league_avg_away_shots_made
    )
    home_stats["home_chance_suppression_eff"] = (
        home_stats["avg_home_shots_conceded"] / league_avg_away_shots_conceded
    )
    away_stats["away_chance_creation_eff"] = (
        away_stats["avg_away_shots_made"] / league_avg_home_shots_made
    )
    away_stats["away_chance_suppression_eff"] = (
        away_stats["avg_away_shots_conceded"] / league_avg_home_shots_conceded
    )

    # Calculate attacking and defensive efficiency
    home_stats["home_attack_eff"] = home_stats["avg_home_goals_scored"] / home_stats[
        "avg_home_shots_made"
    ].replace(0, np.nan)

    home_stats["home_defense_eff"] = home_stats["avg_home_goals_conceded"] / home_stats[
        "avg_home_shots_conceded"
    ].replace(0, np.nan)

    away_stats["away_attack_eff"] = away_stats["avg_away_goals_scored"] / away_stats[
        "avg_away_shots_made"
    ].replace(0, np.nan)

    away_stats["away_defense_eff"] = away_stats["avg_away_goals_conceded"] / away_stats[
        "avg_away_shots_conceded"
    ].replace(0, np.nan)

    # Fill NaN values with 0 (for teams with 0 shots)
    home_stats = home_stats.fillna(0)
    away_stats = away_stats.fillna(0)

    return home_stats, away_stats


def calculate_league_table(matches_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the league table from match results.

    Calculates points (3 for win, 1 for draw, 0 for loss) and sorts by:
    1. Points (descending)
    2. Goal Difference (descending)
    3. Goals For (descending)

    Args:
        matches_df: DataFrame with match results
                   Expected columns: "Home Team", "Away Team", "Home Goals",
                                    "Away Goals", "Result" (H/A/D)

    Returns:
        DataFrame with league table including columns:
        - Team
        - Played
        - Wins
        - Draws
        - Losses
        - Goals For
        - Goals Against
        - Goal Difference
        - Points
        - Position
    """
    teams = matches_df["Home Team"].unique()
    league_table = pd.DataFrame(
        {
            "Team": teams,
            "Played": 0,
            "Wins": 0,
            "Draws": 0,
            "Losses": 0,
            "Goals For": 0,
            "Goals Against": 0,
            "Goal Difference": 0,
            "Points": 0,
        }
    )
    league_table.set_index("Team", inplace=True)

    for _, match in matches_df.iterrows():
        home_team = match["Home Team"]
        away_team = match["Away Team"]
        home_goals = match["Home Goals"]
        away_goals = match["Away Goals"]
        result = match["Result"]

        # Update match counts
        league_table.at[home_team, "Played"] += 1
        league_table.at[away_team, "Played"] += 1

        # Update goals
        league_table.at[home_team, "Goals For"] += home_goals
        league_table.at[home_team, "Goals Against"] += away_goals
        league_table.at[away_team, "Goals For"] += away_goals
        league_table.at[away_team, "Goals Against"] += home_goals

        # Update wins/draws/losses and points
        if result == "H":
            league_table.at[home_team, "Wins"] += 1
            league_table.at[away_team, "Losses"] += 1
            league_table.at[home_team, "Points"] += 3
        elif result == "A":
            league_table.at[away_team, "Wins"] += 1
            league_table.at[home_team, "Losses"] += 1
            league_table.at[away_team, "Points"] += 3
        else:  # Draw
            league_table.at[home_team, "Draws"] += 1
            league_table.at[away_team, "Draws"] += 1
            league_table.at[home_team, "Points"] += 1
            league_table.at[away_team, "Points"] += 1

    # Calculate goal difference
    league_table["Goal Difference"] = (
        league_table["Goals For"] - league_table["Goals Against"]
    )

    # Sort by points, goal difference, and goals for
    league_table = league_table.sort_values(
        by=["Points", "Goal Difference", "Goals For"], ascending=False
    )

    # Add position column
    league_table["Position"] = range(1, len(league_table) + 1)

    return league_table.reset_index()
