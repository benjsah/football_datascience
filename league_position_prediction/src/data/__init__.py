"""
Data loading and processing module
"""

from .loader import (
    load_fixture_csv,
    load_match_statistics,
    normalize_team_names,
    prepare_match_statistics,
    load_and_process_league_data,
)

__all__ = [
    "load_fixture_csv",
    "load_match_statistics",
    "normalize_team_names",
    "prepare_match_statistics",
    "load_and_process_league_data",
]
