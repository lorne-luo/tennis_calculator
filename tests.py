import unittest
from unittest import mock

from main import validate_input, parse_file
from models import Tournament, Match


class MainTestCase(unittest.TestCase):
    file_path = 'full_tournament.txt'

    def test_input(self):
        self.assertFalse(validate_input(['main.py']))
        self.assertFalse(validate_input(['main.py', 'not exist.txt']))
        self.assertEqual(self.file_path, validate_input(['main.py', self.file_path]))

    def test_parse_file(self):
        tournament = parse_file(self.file_path)
        # self.assertEqual(len(tournament.matches), 2)
        # todo more


class TournamentTestCase(unittest.TestCase):
    tournament = Tournament()

    def test_create_match(self):
        match_number = 1
        self.assertEqual(self.tournament.match_count, 0)
        self.tournament.create_match(match_number, 'Player A', 'Player B')
        self.assertEqual(self.tournament.match_count, 1)
        self.assertTrue(self.tournament.get_match(match_number))


class MatchTestCase(unittest.TestCase):
    match = Match(1, 'Player A', 'Player B')

    def test_init(self):
        self.assertEqual(self.match.set_score1, 0)
        self.assertEqual(self.match.set_score2, 0)
        self.assertEqual(self.match.get_winner(), None)

    def test_create_set(self):
        # get init set
        self.assertFalse(self.match.get_set(next=False))
        current_set = self.match.get_set()
        self.assertEqual(current_set.set_number, 1)
        self.assertEqual(self.match.current_set_number, 1)

        # get next set
        # todo

    @mock.patch("models.Match.set_score1", mock.PropertyMock(return_value=0))
    @mock.patch("models.Match.set_score2", mock.PropertyMock(return_value=2))
    def test_get_winner1(self):
        self.assertEqual(self.match.get_winner(), self.match.player2)

    @mock.patch("models.Match.set_score1", mock.PropertyMock(return_value=2))
    @mock.patch("models.Match.set_score2", mock.PropertyMock(return_value=1))
    def test_get_winner2(self):
        self.assertEqual(self.match.get_winner(), self.match.player1)

    @mock.patch("models.Match.set_score1", mock.PropertyMock(return_value=1))
    @mock.patch("models.Match.set_score2", mock.PropertyMock(return_value=1))
    def test_get_winner3(self):
        self.assertEqual(self.match.get_winner(), None)

    def test_add_point(self):
        # todo
        pass
    def test_add_point(self):
        # todo
        pass
