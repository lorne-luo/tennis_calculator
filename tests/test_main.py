import unittest
from collections import OrderedDict
from unittest import mock

from main import validate_input, parse_file
from models.game import Game
from models.set import Set
from models.match import Match
from models.tournament import Tournament


class MainTestCase(unittest.TestCase):
    file_path = 'full_tournament.txt'

    def test_input(self):
        self.assertFalse(validate_input(['main.py']))
        self.assertFalse(validate_input(['main.py', 'not exist.txt']))
        self.assertEqual(self.file_path, validate_input(['main.py', self.file_path]))

    def test_parse_file(self):
        tournament = parse_file(self.file_path)
        self.assertEqual(len(tournament.matches), 2)

        match1 = tournament.get_match(1)
        match2 = tournament.get_match(2)

        self.assertEqual(match1.set_count, 2)
        self.assertEqual(str(match1.get_set(1)), '0 - 6')
        self.assertEqual(str(match1.get_set(2)), '0 - 6')
        self.assertEqual(match1.get_set(3), None)
        self.assertEqual(str(match1), 'Person A vs Person B: 0 - 6, 0 - 6')
        self.assertEqual(match1.get_winner(), 'Person B')

        # todo In the deciding set (if the players get to 1 set each), games continue to play as normal without tie breaker until someone wins by 2 games.
        self.assertEqual(match2.set_count, 3)
        self.assertEqual(str(match2), 'Person A vs Person C: 6 - 7, 6 - 0, 6 - 8')
