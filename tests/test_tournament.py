import unittest
from unittest import mock

from main import validate_input, parse_file
from models.game import Game
from models.set import Set
from models.match import Match
from models.tournament import Tournament


class TournamentTestCase(unittest.TestCase):
    tournament = Tournament()

    def test_create_match(self):
        match_number = 1
        self.assertEqual(self.tournament.match_count, 0)
        self.tournament.create_match(match_number, 'Player A', 'Player B')
        self.assertEqual(self.tournament.match_count, 1)
        self.assertTrue(self.tournament.get_match(match_number))

