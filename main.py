"""!
@brief Symulator Turnieju Piłkarskiego - moduł główny

Moduł odpowiedzialny za zarządzanie całym turniejem piłkarskim.
Zawiera logikę przepływu turnieju od fazy grupowej do finału.

@author Sebastian Orman, Michał Nowakowski

"""

from models import Team, Match
from utils import save_results
from stats import get_total_goals, generate_stats_report, print_stats_report
import random

def get_teams_from_user():
    """!
    @brief Pobiera od użytkownika nazwy 8 drużyn

    Interaktywnie zbiera nazwy drużyn od użytkownika i tworzy obiekty Team.
    Weryfikuje poprawność danych wejściowych.

    @return List[Team] Lista obiektów Team reprezentujących drużyny
    @throws ValueError Jeśli nazwa drużyny jest pusta
    """
    print("=== Symulator turnieju piłkarskiego reprezentacji ===")
    print("Proszę podać nazwy reprezentacji w języku angielskim:")

    teams = []
    while len(teams) < 8:
        try:
            name = input(f"Wpisz reprezentacje {len(teams) + 1}: ").strip()
            if not name:
                raise ValueError("Nazwa nie może być pusta.")

            team = Team(name)

            if team.fifa_rank == 211:
                print(f"Uwaga: {team.name} nie znaleziono w rankingu FIFA. Przypisujemy najmniejszą pozycje w rankingu(211)")

            print(f"  Dodano: {team.name} (FIFA ranking: {team.fifa_rank})")
            teams.append(team)
        except ValueError as e:
            print(f"Błąd: {e}")
    return teams


def play_group_matches(group_name, teams):
    """!
    @brief Przeprowadza wszystkie mecze w fazie grupowej

    @param group_name str Nazwa grupy (np. 'A', 'B')
    @param teams List[Team] Lista obiektów Team w grupie

    @return List[Match] Lista obiektów Match z rozegranymi meczami
    """
    print(f"\n=== Faza grupowa: Grupa {group_name} ===")
    matches = []
    for i, t1 in enumerate(teams):
        for t2 in teams[i + 1:]:
            match = Match(t1, t2, f"Grupa {group_name}")
            match.play()
            print(match.summary())
            matches.append(match)
    return matches


def sort_group(teams):
    """!
    @brief Sortuje drużyny według zasad klasyfikacji turniejowej

    Kryteria sortowania:
    - Liczba punktów (malejąco)
    - Liczba bramek (malejąco)

    @param teams List[Team] Lista drużyn do posortowania

    @return List[Team] Posortowana lista drużyn
    """
    return sorted(teams, key=lambda t: (t.points, t.goals), reverse=True)


def play_knockout(name, team1, team2):
    """!
    @brief Przeprowadza mecz w fazie pucharowej

    @param name str Nazwa fazy (np. 'Półfinał 1')
    @param team1 Team Pierwsza drużyna
    @param team2 Team Druga drużyna

    @return Match Obiekt reprezentujący rozegrany mecz
    """
    print(f"\n=== {name} ===")
    match = Match(team1, team2, name)
    match.play()
    print(match.summary())
    return match


def main():
    """!
    @brief Główna funkcja uruchamiająca symulator turnieju

    Kolejność działań:
    1. Pobranie drużyn od użytkownika
    2. Losowe przydzielenie do grup
    3. Rozegranie fazy grupowej
    4. Rozegranie fazy pucharowej
    5. Wyświetlenie wyników
    6. Zapis statystyk
    """
    print("=== Symulator Turnieju Piłkarskiego (8 drużyn) ===")
    teams = get_teams_from_user()
    random.shuffle(teams)

    group_a = teams[:4]
    group_b = teams[4:]

    matches_a = play_group_matches("A", group_a)
    top_a = sort_group(group_a)[:2]

    matches_b = play_group_matches("B", group_b)
    top_b = sort_group(group_b)[:2]

    semi1 = play_knockout("Półfinał 1", top_a[0], top_b[1])
    semi2 = play_knockout("Półfinał 2", top_b[0], top_a[1])

    third_place = play_knockout("Mecz o 3. miejsce", semi1.get_loser(), semi2.get_loser())
    final = play_knockout("Finał", semi1.get_winner(), semi2.get_winner())

    print("\n=== 🏆 Końcowa Klasyfikacja ===")
    print(f"🥇 Mistrz: {final.get_winner().name}")
    print(f"🥈 Wicemistrz: {final.get_loser().name}")
    print(f"🥉 Trzecie miejsce: {third_place.get_winner().name}")

    save_results(teams, "data.json")
    print(f"\n📈 Łączna liczba goli w turnieju: {get_total_goals(teams)}")

    report = generate_stats_report(teams)
    print_stats_report(report)


if __name__ == "__main__":
    main()