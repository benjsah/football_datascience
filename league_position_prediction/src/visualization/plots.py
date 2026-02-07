"""
Visualization module for plots and charts.

This module provides functions to visualize team statistics and Monte Carlo results.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional


def plot_team_statistics(home_stats: pd.DataFrame,
                        away_stats: Optional[pd.DataFrame] = None,
                        title: str = "Team Statistics",
                        figsize: tuple = (14, 10)) -> None:
    """
    Create scatter plot of team statistics.
    
    Args:
        home_stats: Home team statistics DataFrame
        away_stats: Away team statistics DataFrame (optional)
        title: Title for the plot
        figsize: Figure size tuple (width, height)
    """
    plt.figure(figsize=figsize)
    
    # Plot home team statistics
    sns.scatterplot(
        data=home_stats,
        x="avg_home_goals_scored",
        y="avg_home_goals_conceded",
        s=100,
        label="Home"
    )
    
    # Annotate with team names
    for idx in range(len(home_stats)):
        team_name = home_stats.index[idx]
        x = home_stats["avg_home_goals_scored"].iloc[idx]
        y = home_stats["avg_home_goals_conceded"].iloc[idx]
        plt.text(x, y, team_name, fontsize=9, ha="right")
    
    plt.title(title)
    plt.xlabel("Average Goals Scored")
    plt.ylabel("Average Goals Conceded")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_position_probabilities_heatmap(position_probs: pd.DataFrame,
                                      title: str = "Probability of Final League Positions",
                                      figsize: tuple = (16, 10),
                                      annot_fmt: str = ".2%") -> None:
    """
    Create heatmap of position probabilities.
    
    Args:
        position_probs: DataFrame with shape (n_teams, n_positions)
                       containing probability values
        title: Title for the heatmap
        figsize: Figure size tuple (width, height)
        annot_fmt: Format string for annotations
    """
    plt.figure(figsize=figsize)
    
    # Create heatmap
    ax = sns.heatmap(
        position_probs,
        annot=True,
        fmt=annot_fmt,
        cmap="YlGnBu",
        cbar_kws={"label": "Probability"},
        linewidths=0.5,
        linecolor="gray"
    )
    
    plt.title(title, fontsize=16, fontweight="bold")
    plt.xlabel("Final Position", fontsize=12)
    plt.ylabel("Team", fontsize=12)
    
    # Move x-axis to top
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    
    # Rotate labels
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    plt.show()


def plot_team_position_distribution(position_probs: pd.DataFrame,
                                   team: str,
                                   figsize: tuple = (12, 6)) -> None:
    """
    Create bar plot of position probability distribution for a single team.
    
    Args:
        position_probs: DataFrame with position probabilities
        team: Team name
        figsize: Figure size tuple (width, height)
    """
    team_probs = position_probs.loc[team]
    
    plt.figure(figsize=figsize)
    plt.bar(team_probs.index, team_probs.values, color="steelblue", alpha=0.7)
    
    plt.title(f"{team} - Final Position Probability Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Final Position", fontsize=12)
    plt.ylabel("Probability", fontsize=12)
    plt.xticks(team_probs.index)
    plt.grid(True, alpha=0.3, axis="y")
    
    # Format y-axis as percentage
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: "{:0.1%}".format(y)))
    
    plt.tight_layout()
    plt.show()


def plot_multiple_teams_distribution(position_probs: pd.DataFrame,
                                    teams: list,
                                    figsize: tuple = (14, 8)) -> None:
    """
    Create line plot comparing position distributions for multiple teams.
    
    Args:
        position_probs: DataFrame with position probabilities
        teams: List of team names to plot
        figsize: Figure size tuple (width, height)
    """
    plt.figure(figsize=figsize)
    
    for team in teams:
        if team in position_probs.index:
            team_probs = position_probs.loc[team]
            plt.plot(
                team_probs.index,
                team_probs.values,
                marker="o",
                label=team,
                linewidth=2,
                markersize=6
            )
    
    plt.title("Final Position Probability Distribution - Multiple Teams", 
              fontsize=14, fontweight="bold")
    plt.xlabel("Final Position", fontsize=12)
    plt.ylabel("Probability", fontsize=12)
    plt.xticks(position_probs.columns)
    plt.grid(True, alpha=0.3)
    plt.legend(loc="best")
    
    # Format y-axis as percentage
    ax = plt.gca()
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: "{:0.1%}".format(y)))
    
    plt.tight_layout()
    plt.show()
