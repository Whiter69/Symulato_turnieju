"""
Moduł pomocniczy z funkcjami do zapisu danych.
"""

import json

def save_results(teams, filename="tournament_results.json"):
    """
    Zapisuje wyniki turnieju do pliku JSON.
    """
    data = [
        {
            "team": t.name,
            "fifa_rank": t.fifa_rank,
            "tournament_points": t.points,
            "goals_scored": t.goals
        } for t in teams
    ]

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\nResults saved to: {filename}")
    except IOError as e:
        print(f"Error saving file: {e}")