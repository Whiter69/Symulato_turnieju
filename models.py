"""
Moduł zawierający klasy reprezentujące drużyny i mecze.
"""

import random
from transfermarkt_rankings import get_full_rankings, normalize_country_name, get_team_rank

class Team:
    """
    Klasa reprezentująca drużynę piłkarską.
    """

    def __init__(self, name):
        """
        Inicjalizacja drużyny.
        """
        self.original_name = name
        self.name = normalize_country_name(name)
        self.points = 0
        self.goals = 0
        self.fifa_rank = self._get_fifa_rank()

    def _get_fifa_rank(self):
        """
        Pobiera ranking FIFA dla drużyny.
        """
        if not hasattr(Team, '_rankings'):
            Team._rankings = get_full_rankings()

        return get_team_rank(self.original_name, Team._rankings)

    def get_strength(self):
        """
        Oblicza siłę drużyny na podstawie rankingu (1-211)
        """
        if self.fifa_rank <= 10:
            return 0.9 - (self.fifa_rank * 0.02)
        elif self.fifa_rank <= 50:
            return 0.7 - ((self.fifa_rank - 10) * 0.01)
        else:
            return 0.3 - ((self.fifa_rank - 50) * 0.0025)

    def __str__(self):
        return f"{self.name} – {self.points} pts, {self.goals} goals (FIFA rank: {self.fifa_rank})"
class Match:
    """
    Klasa reprezentująca mecz piłkarski.
    """

    def __init__(self, team1, team2, phase="Faza grupowa"):
        self.team1 = team1
        self.team2 = team2
        self.score = (0, 0)
        self.phase = phase
        self.penalty_result = None

    def play(self):
        """Symuluje mecz z uwzględnieniem rankingu FIFA"""
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
        """Symuluje rzuty karne"""
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
        if self.score[0] > self.score[1]:
            return self.team1
        elif self.score[0] < self.score[1]:
            return self.team2
        else:
            return self.team1 if self.penalty_result[0] > self.penalty_result[1] else self.team2

    def get_loser(self):
        winner = self.get_winner()
        return self.team2 if winner == self.team1 else self.team1

    def summary(self):
        result = f"[{self.phase}] {self.team1.name} {self.score[0]} : {self.score[1]} {self.team2.name}"
        if self.penalty_result:
            result += f" ⚽ (karne: {self.team1.name} {self.penalty_result[0]} - {self.penalty_result[1]} {self.team2.name})"
        return result