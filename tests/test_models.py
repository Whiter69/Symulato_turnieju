"""
Testy jednostkowe dla modułu models.py
"""

import unittest
import random
from unittest.mock import patch
from models import Team, Match

class TestTeam(unittest.TestCase):
    """Testy dla klasy Team."""

    @patch('models.get_full_rankings')
    @patch('models.get_team_rank')
    def setUp(self, mock_get_team_rank, mock_get_full_rankings):
        """Przygotowanie danych testowych."""
        mock_get_full_rankings.return_value = [{'country': 'Poland', 'rank': 34}]
        mock_get_team_rank.return_value = 34
        self.team = Team("Polska")

    def test_team_initialization(self):
        """Test poprawnej inicjalizacji drużyny."""
        self.assertEqual(self.team.name, "Poland")
        self.assertEqual(self.team.points, 0)
        self.assertEqual(self.team.goals, 0)
        self.assertEqual(self.team.fifa_rank, 34)

    def test_get_strength(self):
        """Test obliczania siły drużyny."""
        self.assertAlmostEqual(self.team.get_strength(), 0.46, delta=0.01)

    def test_str_representation(self):
        """Test reprezentacji tekstowej."""
        self.assertEqual(str(self.team), "Poland – 0 pts, 0 goals (FIFA rank: 34)")

class TestMatch(unittest.TestCase):
    """Testy dla klasy Match."""

    def setUp(self):
        """Przygotowanie danych testowych."""
        self.team1 = Team("Brazylia")
        self.team1.fifa_rank = 1
        self.team2 = Team("Panama")
        self.team2.fifa_rank = 100
        self.match = Match(self.team1, self.team2)

    def test_match_initialization(self):
        """Test inicjalizacji meczu."""
        self.assertEqual(self.match.team1.name, "Brazil")
        self.assertEqual(self.match.phase, "Faza grupowa")
        self.assertEqual(self.match.score, (0, 0))

    def test_play_group_match(self):
        """Test symulacji meczu grupowego."""
        random.seed(42)
        self.match.play()

        self.assertTrue(0 <= self.match.score[0] <= 7)
        self.assertTrue(0 <= self.match.score[1] <= 7)

        self.assertEqual(self.team1.goals, self.match.score[0])
        self.assertEqual(self.team2.goals, self.match.score[1])

    def test_play_knockout_match(self):
        """Test symulacji meczu pucharowego."""
        knockout = Match(self.team1, self.team2, "Półfinał")
        random.seed(123)
        knockout.play()

        if knockout.score[0] == knockout.score[1]:
            self.assertIsNotNone(knockout.penalty_result)
            self.assertEqual(len(knockout.penalty_result), 2)

    def test_get_winner(self):
        """Test wyłaniania zwycięzcy."""
        self.match.score = (2, 1)
        self.assertEqual(self.match.get_winner(), self.team1)

        self.match.score = (1, 1)
        self.match.penalty_result = (3, 5)
        self.assertEqual(self.match.get_winner(), self.team2)

    def test_summary(self):
        """Test podsumowania meczu."""
        self.match.score = (3, 2)
        self.assertEqual(
            self.match.summary(),
            "[Faza grupowa] Brazil 3 : 2 Panama"
        )

if __name__ == "__main__":
    unittest.main()