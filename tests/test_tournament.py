import unittest
from unittest import mock

from main import validate_input, parse_file, capture_input
from models.game import Game
from models.set import Set
from models.match import Match
from models.tournament import Tournament


class TournamentTestCase(unittest.TestCase):
    tournament = Tournament()

    def test_create_match(self):
        match_number = 1
        self.assertEqual(self.tournament.match_count, 0)
        self.tournament.create_match(match_number, "Player A", "Player B")
        self.assertEqual(self.tournament.match_count, 1)
        self.assertTrue(self.tournament.get_match(match_number))


class MainTestCase(unittest.TestCase):
    file_path = "full_tournament.txt"

    def test_input(self):
        self.assertFalse(validate_input(["main.py"]))
        self.assertFalse(validate_input(["main.py", "not exist.txt"]))
        self.assertEqual(self.file_path, validate_input(["main.py", self.file_path]))

        self.assertEqual(("player", "Person A"), capture_input("Games Player Person A"))
        self.assertEqual(("match", 1), capture_input("Score Match 01"))
        self.assertEqual(("exit", None), capture_input("Exit"))
        self.assertEqual((None, None), capture_input("invalid input"))

    def test_parse_file(self):
        tournament = parse_file(self.file_path)
        self.assertEqual(len(tournament.matches), 2)

        match1 = tournament.get_match(1)
        match2 = tournament.get_match(2)

        # match's set score
        self.assertEqual(match1.get_set(1).get_winner(), match1.player2)
        self.assertEqual(match1.get_set(2).get_winner(), match1.player2)

        self.assertEqual(match1.set_score1, 0)
        self.assertEqual(match1.set_score2, 2)

        # winner
        self.assertEqual(match2.get_set(1).get_winner(), match2.player2)
        self.assertEqual(match2.get_set(2).get_winner(), match2.player1)
        self.assertEqual(match2.get_set(3).get_winner(), match2.player2)

        # set result
        self.assertEqual(match2.set_score1, 1)
        self.assertEqual(match2.set_score2, 2)
        self.assertEqual(match1.set_count, 2)
        self.assertEqual(str(match1.get_set(1)), "0 - 6")
        self.assertEqual(str(match1.get_set(2)), "0 - 6")
        self.assertEqual(match1.get_set(3), None)

        # match result
        self.assertEqual(str(match1), "Person A vs Person B: 0 - 6, 0 - 6")
        self.assertEqual(match1.get_winner(), "Person B")
        self.assertEqual(match2.set_count, 3)
        self.assertEqual(str(match2), "Person A vs Person C: 6 - 7, 6 - 0, 6 - 8")
        self.assertTrue(match2.get_set(3).is_deciding)  # deciding set
        self.assertEqual(match2.get_set(4), None)

        # get player point
        self.assertEqual(match1.get_player_point(match1.player1), (0, 48))
        self.assertEqual(match1.get_player_point(match1.player2), (48, 0))
        self.assertEqual(tournament.get_player_point(match1.player1), (80, 114))
        self.assertEqual(tournament.get_player_point(match2.player2), (66, 80))
        self.assertEqual(tournament.get_player_point('Not exist player'), (None, None))
