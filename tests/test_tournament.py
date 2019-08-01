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
        self.tournament.create_match(match_number, 'Player A', 'Player B')
        self.assertEqual(self.tournament.match_count, 1)
        self.assertTrue(self.tournament.get_match(match_number))



class MainTestCase(unittest.TestCase):
    file_path = 'full_tournament.txt'

    def test_input(self):
        self.assertFalse(validate_input(['main.py']))
        self.assertFalse(validate_input(['main.py', 'not exist.txt']))
        self.assertEqual(self.file_path, validate_input(['main.py', self.file_path]))

        self.assertEqual(('player','Person A'),capture_input('Games Player Person A'))
        self.assertEqual(('match', 1),capture_input('Score Match 01'))
        self.assertEqual(('exit', None),capture_input('Exit'))
        self.assertEqual((None, None),capture_input('invalid input'))


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

        self.assertEqual(match2.get_set(1).get_winner(), match2.player2)
        self.assertEqual(match2.get_set(2).get_winner(), match2.player1)
        self.assertEqual(match2.get_set(3).get_winner(), match2.player2)

        self.assertEqual(match2.set_score1, 1)
        self.assertEqual(match2.set_score2, 2)


        self.assertEqual(match1.set_count, 2)
        self.assertEqual(str(match1.get_set(1)), '0 - 6')
        self.assertEqual(str(match1.get_set(2)), '0 - 6')
        self.assertEqual(match1.get_set(3), None)
        self.assertEqual(str(match1), 'Person A vs Person B: 0 - 6, 0 - 6')
        self.assertEqual(match1.get_winner(), 'Person B')

        # todo In the deciding set (if the players get to 1 set each), games continue to play as normal without tie breaker until someone wins by 2 games.
        self.assertEqual(match2.set_count, 3)
        self.assertEqual(str(match2), 'Person A vs Person C: 6 - 7, 6 - 0, 6 - 8')