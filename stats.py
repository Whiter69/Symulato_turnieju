"""!
@brief Rozbudowany moduł statystyk z wizualizacją danych

Moduł zawiera funkcje do:
- Obliczania statystyk turnieju
- Generowania wykresów
- Tworzenia raportów

@requires matplotlib.pyplot
@requires numpy
@requires functools.reduce
"""

from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from models import Team

def get_total_goals(teams: List[Team]) -> int:
    """!
    @brief Oblicza łączną liczbę goli w turnieju

    @param teams List[Team] Lista obiektów Team reprezentujących drużyny
    @return int Suma goli wszystkich drużyn
    """
    return reduce(lambda acc, t: acc + t.goals, teams, 0)

def get_average_goals_per_team(teams: List[Team]) -> float:
    """!
    @brief Oblicza średnią liczbę goli na drużynę

    @param teams List[Team] Lista obiektów Team
    @return float Średnia liczba goli
    @retval 0 Jeśli lista drużyn jest pusta
    """
    return get_total_goals(teams) / len(teams) if teams else 0

def get_goal_distribution(teams: List[Team]) -> dict:
    """!
    @brief Zwraca rozkład goli według drużyn

    @param teams List[Team] Lista obiektów Team
    @return dict Słownik w formacie {nazwa_drużyny: liczba_goli}
    """
    return {team.name: team.goals for team in teams}

def get_top_scorers(teams: List[Team], top_n: int = 5) -> List[Team]:
    """!
    @brief Zwraca listę najlepszych strzelców

    @param teams List[Team] Lista obiektów Team
    @param top_n int Liczba najlepszych strzelców do zwrócenia (domyślnie 5)
    @return List[Team] Posortowana lista drużyn według liczby goli
    """
    return sorted(teams, key=lambda t: t.goals, reverse=True)[:top_n]

def plot_goals_distribution(teams: List[Team]):
    """!
    @brief Generuje i zapisuje wykres słupkowy rozkładu goli

    @details Wykres zawiera:
    - Słupki przedstawiające liczbę goli każdej drużyny
    - Etykiety z dokładnymi wartościami nad słupkami
    - Automatyczne dopasowanie rozmiaru wykresu

    @param teams List[Team] Lista obiektów Team
    """
    teams_sorted = sorted(teams, key=lambda t: t.goals, reverse=True)
    names = [t.name for t in teams_sorted]
    goals = [t.goals for t in teams_sorted]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(names, goals, color='skyblue')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)}',
                 ha='center', va='bottom')

    plt.title('Rozkład goli drużyn w turnieju', fontsize=14)
    plt.xlabel('Drużyna', fontsize=12)
    plt.ylabel('Liczba goli', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('goals_distribution.png')
    plt.close()

def plot_rank_vs_performance(teams: List[Team]):
    """!
    @brief Generuje wykres porównujący ranking FIFA z osiągnięciami

    @details Tworzy podwójny wykres punktowy:
    1. Ranking FIFA vs punkty w turnieju
    2. Ranking FIFA vs liczba goli
    Zawiera etykiety z nazwami drużyn.

    @param teams List[Team] Lista obiektów Team
    @post Zapisuje wykres do pliku rank_vs_performance.png
    """
    teams_sorted = sorted(teams, key=lambda t: t.fifa_rank)
    ranks = [t.fifa_rank for t in teams_sorted]
    points = [t.points for t in teams_sorted]
    goals = [t.goals for t in teams_sorted]
    names = [t.name for t in teams_sorted]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Wykres punktów vs ranking
    scatter1 = ax1.scatter(ranks, points, color='blue')
    ax1.set_title('Ranking FIFA vs Punkty w turnieju', pad=20)
    ax1.set_xlabel('Ranking FIFA (mniejszy = lepszy)')
    ax1.set_ylabel('Punkty w turnieju')
    ax1.invert_xaxis()

    # Dodanie etykiet z nazwami drużyn
    for i, (rank, point, name) in enumerate(zip(ranks, points, names)):
        ax1.annotate(name,
                     (rank, point),
                     textcoords="offset points",
                     xytext=(0, 10 if i % 2 == 0 else -15),
                     ha='center',
                     fontsize=8,
                     alpha=0.7)

    # Wykres goli vs ranking
    scatter2 = ax2.scatter(ranks, goals, color='green')
    ax2.set_title('Ranking FIFA vs Liczba goli', pad=20)
    ax2.set_xlabel('Ranking FIFA (mniejszy = lepszy)')
    ax2.set_ylabel('Gole w turnieju')
    ax2.invert_xaxis()

    for i, (rank, goal, name) in enumerate(zip(ranks, goals, names)):
        ax2.annotate(name,
                     (rank, goal),
                     textcoords="offset points",
                     xytext=(0, 10 if i % 2 == 0 else -15),
                     ha='center',
                     fontsize=8,
                     alpha=0.7)

    plt.tight_layout()
    plt.savefig('rank_vs_performance.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_stats_report(teams: List[Team]) -> dict:
    """!
    @brief Generuje kompleksowy raport statystyczny

    @details Raport zawiera:
    - Łączną i średnią liczbę goli
    - Listę najlepszych strzelców
    - Listę drużyn z najlepszymi wynikami względem rankingu
    - Automatycznie generuje wykresy

    @param teams List[Team] Lista obiektów Team


    """
    report = {
        'total_goals': get_total_goals(teams),
        'average_goals_per_team': round(get_average_goals_per_team(teams), 2),
        'top_scorers': [(t.name, t.goals) for t in get_top_scorers(teams)],
        'best_performance_by_rank': sorted(
            teams,
            key=lambda t: (t.points, t.goals),
            reverse=True
        )[:5]
    }

    plot_goals_distribution(teams)
    plot_rank_vs_performance(teams)

    return report

def print_stats_report(report: dict):
    """!
    @brief Wyświetla raport statystyczny w czytelnej formie

    @param report dict Słownik z raportem wygenerowanym przez generate_stats_report()
    """
    print("\n=== RAPORT STATYSTYCZNY TURNIEJU ===")
    print(f"Łączna liczba goli: {report['total_goals']}")
    print(f"Średnia goli na drużynę: {report['average_goals_per_team']}")

    print("\nNajlepsi strzelcy:")
    for i, (name, goals) in enumerate(report['top_scorers'], 1):
        print(f"{i}. {name}: {goals} goli")

    print("\nNajlepsze performanse względem rankingu FIFA:")
    for team in report['best_performance_by_rank']:
        print(f"- {team.name} (rank {team.fifa_rank}): {team.points} pkt, {team.goals} goli")

    print("\nWykresy statystyczne zostały zapisane jako:")
    print("- goals_distribution.png")
    print("- rank_vs_performance.png")