"""
Moduł z funkcjami statystycznymi.
"""

from functools import reduce

def get_total_goals(teams):
    """
    Oblicza łączną liczbę goli w turnieju.

    Args:
        teams (list): Lista obiektów Team

    Returns:
        int: Suma goli wszystkich drużyn
    """
    return reduce(lambda acc, t: acc + t.goals, teams, 0)