"""
Monte Carlo simulation engine for season prediction.

This module runs multiple simulations of the remaining season matches
to estimate the probability distribution of final league positions.
"""

import numpy as np
import pandas as pd
from typing import Tuple, List

from .poisson import simulate_match, get_match_result
from ..preprocessing.statistics import calculate_league_table


def simulate_season(
    remaining_matches: pd.DataFrame, home_stats: pd.DataFrame, away_stats: pd.DataFrame
) -> pd.DataFrame:
    """
    Simulate all remaining matches of the season.

    Args:
        remaining_matches: DataFrame with remaining matches
                          Columns: "Home Team", "Away Team"
        home_stats: DataFrame with home team statistics
        away_stats: DataFrame with away team statistics

    Returns:
        DataFrame with simulated results including columns:
        "Home Team", "Away Team", "Home Goals", "Away Goals", "Result"
    """
    simulated_results = remaining_matches.copy()

    # Add columns for results
    simulated_results["Home Goals"] = 0
    simulated_results["Away Goals"] = 0
    simulated_results["Result"] = ""

    # Simulate each match
    for index, row in simulated_results.iterrows():
        home_team = row["Home Team"]
        away_team = row["Away Team"]

        # Simulate match
        home_goals, away_goals = simulate_match(
            home_team, away_team, home_stats, away_stats
        )

        # Store results
        simulated_results.at[index, "Home Goals"] = home_goals
        simulated_results.at[index, "Away Goals"] = away_goals
        simulated_results.at[index, "Result"] = get_match_result(home_goals, away_goals)

    return simulated_results


def monte_carlo_simulation(
    fixtures_df: pd.DataFrame,
    played_matches_df: pd.DataFrame,
    home_stats: pd.DataFrame,
    away_stats: pd.DataFrame,
    n_simulations: int = 1000,
    random_seed: int = None,
) -> Tuple[List[pd.DataFrame], List[pd.DataFrame]]:
    """
    Run Monte Carlo simulation of remaining season matches.

    Runs n_simulations complete simulations of the remaining season matches,
    calculating the final league table for each simulation.

    Args:
        fixtures_df: DataFrame with all season fixtures
        played_matches_df: DataFrame with already played matches
        home_stats: DataFrame with home team statistics
        away_stats: DataFrame with away team statistics
        n_simulations: Number of simulations to run
        random_seed: Seed for random number generator (optional)

    Returns:
        Tuple of:
        - List of league table DataFrames (one per simulation)
        - List of full season results DataFrames (one per simulation)
    """
    if random_seed is not None:
        np.random.seed(random_seed)

    league_tables = []
    full_season_results_list = []

    for simulation_number in range(n_simulations):
        # Identify remaining matches
        remaining_matches = fixtures_df[fixtures_df["Result"].isnull()].reset_index(
            drop=True
        )
        remaining_matches = remaining_matches[["Home Team", "Away Team"]]

        # Simulate remaining matches
        simulated_results = simulate_season(remaining_matches, home_stats, away_stats)

        # Combine with played matches
        full_season_results = pd.concat(
            [played_matches_df, simulated_results], ignore_index=True
        )
        full_season_results_list.append(full_season_results)

        # Calculate league table
        league_table = calculate_league_table(full_season_results)
        league_tables.append(league_table)

    return league_tables, full_season_results_list


def calculate_position_probabilities(
    league_tables: List[pd.DataFrame],
    current_league_table: pd.DataFrame = None,
    team_names: list = None,
) -> pd.DataFrame:
    """
    Calculate probability of each team finishing in each final position.

    Args:
        league_tables: List of league table DataFrames from simulations
        current_league_table: Current season league table to determine team order
                             If provided, results will be sorted by current position
        team_names: List of all team names (in desired order)
                   If None, derived from current league table or first league table

    Returns:
        DataFrame with shape (n_teams, n_positions) containing probabilities
        Rows are teams (ordered by current league position), columns are final positions (1-18)
    """
    if not league_tables:
        raise ValueError("league_tables cannot be empty")

    # Get team names in order of current league position if available
    if current_league_table is not None:
        team_names = current_league_table["Team"].tolist()
    elif team_names is None:
        team_names = league_tables[0]["Team"].tolist()

    n_teams = len(team_names)
    n_positions = n_teams

    # Initialize position probability DataFrame
    position_probs = pd.DataFrame(
        0.0, index=team_names, columns=range(1, n_positions + 1)
    )

    # Count final positions across simulations
    for league_table in league_tables:
        for _, row in league_table.iterrows():
            team = row["Team"]
            position = int(row["Position"])
            if team in position_probs.index:
                position_probs.at[team, position] += 1

    # Normalize to get probabilities
    position_probs = position_probs.div(position_probs.sum(axis=1), axis=0)

    return position_probs


def get_team_final_position_stats(position_probs: pd.DataFrame, team: str) -> dict:
    """
    Calculate statistics for a team's final position distribution.

    Args:
        position_probs: DataFrame of position probabilities
        team: Team name

    Returns:
        Dictionary with statistics:
        - most_likely_position: Position with highest probability
        - most_likely_prob: Probability of most likely position
        - mean_position: Expected final position
        - std_position: Standard deviation of final position
        - prob_top_4: Probability of finishing in top 4
        - prob_top_6: Probability of finishing in top 6
    """
    team_probs = position_probs.loc[team]
    positions = np.array(position_probs.columns)
    probs = team_probs.values

    # Most likely position
    most_likely_idx = np.argmax(probs)
    most_likely_position = positions[most_likely_idx]
    most_likely_prob = probs[most_likely_idx]

    # Mean and std of position
    mean_position = np.sum(positions * probs)
    std_position = np.sqrt(np.sum((positions - mean_position) ** 2 * probs))

    # Probability of top positions
    prob_top_4 = team_probs[:4].sum()
    prob_top_6 = team_probs[:6].sum()

    return {
        "most_likely_position": int(most_likely_position),
        "most_likely_prob": round(most_likely_prob, 4),
        "mean_position": round(mean_position, 2),
        "std_position": round(std_position, 2),
        "prob_top_4": round(prob_top_4, 4),
        "prob_top_6": round(prob_top_6, 4),
    }
