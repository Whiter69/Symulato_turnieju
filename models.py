"""!
@brief Moduł zawierający klasy reprezentujące drużyny i mecze piłkarskie

Zawiera:
- Klasa Team: Reprezentuje drużynę piłkarską z jej statystykami
- Klasa Match: Reprezentuje mecz piłkarski i jego wynik
"""

import random
from transfermarkt_rankings import get_full_rankings, normalize_country_name, get_team_rank

class Team:
    """!
    @brief Klasa reprezentująca drużynę piłkarską

    Przechowuje informacje o drużynie i oblicza jej siłę na podstawie rankingu FIFA.
    """

    def __init__(self, name):
        """!
        @brief Inicjalizacja obiektu drużyny

        @param name str Nazwa drużyny w formacie do normalizacji
        """
        self.original_name = name
        self.name = normalize_country_name(name)
        self.points = 0  #!< Punkty zdobyte w turnieju
        self.goals = 0   #!< Bramki zdobyte w turnieju
        self.fifa_rank = self._get_fifa_rank()  #!< Pozycja w rankingu FIFA

    def _get_fifa_rank(self):
        """!
        @brief Pobiera ranking FIFA dla drużyny

        @details Wykorzystuje zewnętrzną funkcję get_team_rank() do pobrania rankingu.
        Dla nieznalezionych drużyn zwraca wartość 211 (najniższy możliwy ranking).

        @return int Pozycja w rankingu FIFA
        """
        if not hasattr(Team, '_rankings'):
            Team._rankings = get_full_rankings()

        return get_team_rank(self.original_name, Team._rankings)

    def get_strength(self):
        """!
        @brief Oblicza siłę drużyny w przedziale 0-1

        @details Wzór obliczeniowy:
        - Top 10: 0.9 - (rank * 0.02)
        - Top 50: 0.7 - ((rank-10) * 0.01)
        - Pozostałe: 0.3 - ((rank-50) * 0.0025)

        @return float Wartość siły drużyny (0-1)
        """
        if self.fifa_rank <= 10:
            return 0.9 - (self.fifa_rank * 0.02)
        elif self.fifa_rank <= 50:
            return 0.7 - ((self.fifa_rank - 10) * 0.01)
        else:
            return 0.3 - ((self.fifa_rank - 50) * 0.0025)

    def __str__(self):
        """!
        @brief Reprezentacja tekstowa drużyny

        @return str String w formacie "Nazwa - punkty pts, bramki goals (FIFA rank: X)"
        """
        return f"{self.name} – {self.points} pts, {self.goals} goals (FIFA rank: {self.fifa_rank})"


class Match:
    """!
    @brief Klasa reprezentująca mecz piłkarski

    Zawiera logikę symulacji meczu i rzutów karnych.
    """

    def __init__(self, team1, team2, phase="Faza grupowa"):
        """!
        @brief Inicjalizacja obiektu meczu

        @param team1 Team Pierwsza drużyna
        @param team2 Team Druga drużyna
        @param phase str Faza turnieju (domyślnie "Faza grupowa")
        """
        self.team1 = team1
        self.team2 = team2
        self.score = (0, 0)
        self.phase = phase
        self.penalty_result = None

    def play(self):
        """!
        @brief Symuluje mecz piłkarski

        @details Algorytm symulacji:
        1. Oblicza siłę obu drużyn
        2. Generuje liczbę goli z rozkładu normalnego
        3. Ogranicza wynik do max 7 goli
        4. W fazie grupowej przyznaje punkty
        5. W fazie pucharowej w przypadku remisu przeprowadza rzuty karne
        """
        strength1 = self.team1.get_strength()
        strength2 = self.team2.get_strength()

        avg_goals = 2.5
        lambda1 = avg_goals * (strength1 / (strength1 + strength2))
        lambda2 = avg_goals * (strength2 / (strength1 + strength2))

        g1 = max(0, int(random.gauss(lambda1, 1)))
        g2 = max(0, int(random.gauss(lambda2, 1)))
        g1 = min(g1, 7)
        g2 = min(g2, 7)

        self.score = (g1, g2)
        self.team1.goals += g1
        self.team2.goals += g2

        if self.phase.startswith("Grupa"):
            if g1 > g2:
                self.team1.points += 3
            elif g1 < g2:
                self.team2.points += 3
            else:
                self.team1.points += 1
                self.team2.points += 1
        else:
            if g1 == g2:
                self.play_penalties()

    def play_penalties(self):
        """!
        @brief Symuluje rzuty karne

        @details Każda drużyna wykonuje 5 strzałów:
        - Prawdopodobieństwo trafienia zależy od siły drużyny
        - W przypadku remisu następuje seria "nagłej śmierci"
        """
        print(f"   🔄 Remis! Rzuty karne między {self.team1.name} i {self.team2.name}")

        strength1 = self.team1.get_strength()
        strength2 = self.team2.get_strength()

        prob1 = 0.7 + (strength1 * 0.2)
        prob2 = 0.7 + (strength2 * 0.2)

        p1 = sum(1 for _ in range(5) if random.random() < prob1)
        p2 = sum(1 for _ in range(5) if random.random() < prob2)

        while p1 == p2:
            p1 += 1 if random.random() < prob1 else 0
            p2 += 1 if random.random() < prob2 else 0

        self.penalty_result = (p1, p2)

    def get_winner(self):
        """!
        @brief Określa zwycięzcę meczu

        @details Uwzględnia:
        - Wynik podstawowy
        - Ewentualne rzuty karne

        @return Team Zwycięska drużyna
        """
        if self.score[0] > self.score[1]:
            return self.team1
        elif self.score[0] < self.score[1]:
            return self.team2
        else:
            return self.team1 if self.penalty_result[0] > self.penalty_result[1] else self.team2

    def get_loser(self):
        """!
        @brief Określa przegranego meczu

        @return Team Przegrana drużyna
        """
        winner = self.get_winner()
        return self.team2 if winner == self.team1 else self.team1

    def summary(self):
        """!
        @brief Generuje tekstowe podsumowanie meczu

        @return str String w formacie:
        "[Faza] Drużyna1 X : Y Drużyna2 [⚽ karne: A-B]"
        """
        result = f"[{self.phase}] {self.team1.name} {self.score[0]} : {self.score[1]} {self.team2.name}"
        if self.penalty_result:
            result += f" ⚽ (karne: {self.team1.name} {self.penalty_result[0]} - {self.penalty_result[1]} {self.team2.name})"
        return result