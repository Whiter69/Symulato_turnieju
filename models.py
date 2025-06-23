"""
Moduł zawierający klasy reprezentujące drużyny i mecze.
"""

import random

class Team:
    """
    Klasa reprezentująca drużynę piłkarską.

    Attributes:
        name (str): Nazwa drużyny
        points (int): Liczba punktów w turnieju
        goals (int): Łączna liczba zdobytych goli
    """

    def __init__(self, name):
        """
        Inicjalizacja drużyny.

        Args:
            name (str): Nazwa drużyny
        """
        self.name = name
        self.points = 0
        self.goals = 0

    def __str__(self):
        """
        Reprezentacja tekstowa drużyny.

        Returns:
            str: String w formacie 'Nazwa - X pkt, Y goli'
        """
        return f"{self.name} – {self.points} pkt, {self.goals} goli"

class Match:
    """
    Klasa reprezentująca mecz piłkarski.

    Attributes:
        team1 (Team): Pierwsza drużyna
        team2 (Team): Druga drużyna
        score (tuple): Wynik meczu (gole_team1, gole_team2)
        phase (str): Faza turnieju
        penalty_result (tuple): Wynik rzutów karnych (jeśli były)
    """

    def __init__(self, team1, team2, phase="Faza grupowa"):
        """
        Inicjalizacja meczu.

        Args:
            team1 (Team): Pierwsza drużyna
            team2 (Team): Druga drużyna
            phase (str, optional): Faza turnieju. Domyślnie "Faza grupowa".
        """
        self.team1 = team1
        self.team2 = team2
        self.score = (0, 0)
        self.phase = phase
        self.penalty_result = None

    def play(self):
        """Symuluje rozegranie meczu z losowym wynikiem."""
        g1 = random.randint(0, 5)
        g2 = random.randint(0, 5)
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
        """Symuluje rzuty karne w przypadku remisu w fazie pucharowej."""
        print(f"   🔄 Remis! Rzuty karne między {self.team1.name} i {self.team2.name}")
        p1 = sum(random.choices([0, 1], k=5))
        p2 = sum(random.choices([0, 1], k=5))

        while p1 == p2:
            p1 += random.choice([0, 1])
            p2 += random.choice([0, 1])

        self.penalty_result = (p1, p2)

    def get_winner(self):
        """
        Zwraca zwycięzcę meczu.

        Returns:
            Team: Zwycięska drużyna
        """
        if self.score[0] > self.score[1]:
            return self.team1
        elif self.score[0] < self.score[1]:
            return self.team2
        else:
            return self.team1 if self.penalty_result[0] > self.penalty_result[1] else self.team2

    def get_loser(self):
        """
        Zwazuje przegranego meczu.

        Returns:
            Team: Przegrana drużyna
        """
        winner = self.get_winner()
        return self.team2 if winner == self.team1 else self.team1

    def summary(self):
        """
        Generuje podsumowanie meczu.

        Returns:
            str: Tekstowe podsumowanie meczu
        """
        result = f"[{self.phase}] {self.team1.name} {self.score[0]} : {self.score[1]} {self.team2.name}"
        if self.penalty_result:
            result += f" ⚽ (karne: {self.team1.name} {self.penalty_result[0]} - {self.penalty_result[1]} {self.team2.name})"
        return result