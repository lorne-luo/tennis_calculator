import unittest
from collections import OrderedDict
from unittest import mock

from main import validate_input, parse_file
from models import Tournament, Match, Set, Game


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
        self.assertEqual(self.match.get_set(11), None)

    def test_create_set(self):
        # get init set
        self.match.sets = OrderedDict()
        self.match.current_set_number = None
        self.assertFalse(self.match.create_or_get_set(next=False))
        current_set = self.match.create_or_get_set()
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


class SetTestCase(unittest.TestCase):
    set = Set(Match(1, 'Player A', 'Player B'), 1)

    def test_property(self):
        self.assertEqual(self.set.player1, 'Player A')
        self.assertEqual(self.set.player2, 'Player B')
        self.assertEqual(self.set.get_winner(), None)
        self.assertEqual(self.set.get_game(11), None)

    @mock.patch("models.Set.game_score1", mock.PropertyMock(return_value=0))
    @mock.patch("models.Set.game_score2", mock.PropertyMock(return_value=6))
    def test_get_winner1(self):
        self.assertEqual(self.set.get_winner(), self.set.player2)

    @mock.patch("models.Set.game_score1", mock.PropertyMock(return_value=7))
    @mock.patch("models.Set.game_score2", mock.PropertyMock(return_value=6))
    def test_get_winner2(self):
        self.assertEqual(self.set.get_winner(), self.set.player1)

    @mock.patch("models.Set.game_score1", mock.PropertyMock(return_value=4))
    @mock.patch("models.Set.game_score2", mock.PropertyMock(return_value=6))
    def test_get_winner3(self):
        self.assertEqual(self.set.get_winner(), self.set.player2)

    @mock.patch("models.Set.game_score1", mock.PropertyMock(return_value=5))
    @mock.patch("models.Set.game_score2", mock.PropertyMock(return_value=6))
    def test_get_winner4(self):
        self.assertEqual(self.set.get_winner(), None)

    def test_game(self):
        self.assertEqual(self.set.current_game_number, None)  # game not start yet
        self.assertFalse(self.set.create_or_get_game(next=False))
        current_game = self.set.create_or_get_game()
        self.assertTrue(current_game)

        # get next game
        # todo

    def test_add_point(self):
        # todo
        pass


class GameTestCase(unittest.TestCase):
    game = Game(1, Set(Match(1, 'Player A', 'Player B'), 1))

    def test_init(self):
        self.assertEqual(self.game.player1, 'Player A')
        self.assertEqual(self.game.player2, 'Player B')

    def test_get_winner(self):
        self.game.point1 = 0
        self.game.point2 = 3
        self.assertEqual(str(self.game), '0 - 40')
        self.assertEqual(self.game.get_winner(), None)

        self.game.point1 = 3
        self.game.point2 = 3
        self.assertEqual(self.game.get_winner(), None)
        self.assertEqual(str(self.game), '40 - 40')

        self.game.point1 = 4
        self.game.point2 = 3
        self.assertEqual(self.game.get_winner(), None)
        self.assertEqual(str(self.game), '40* - 40')

        self.game.point1 = 4
        self.game.point2 = 2
        self.assertEqual(self.game.get_winner(), self.game.player1)
        self.assertEqual(str(self.game), 'Game - 30')

        self.game.point1 = 4
        self.game.point2 = 5
        self.assertEqual(self.game.get_winner(), None)
        self.assertEqual(str(self.game), '40 - 40*')

        self.game.point1 = 4
        self.game.point2 = 6
        self.assertEqual(self.game.get_winner(), self.game.player2)
        self.assertEqual(str(self.game), '40 - Game')

        self.game.point1 = self.game.point2 = 6
        self.assertEqual(self.game.get_winner(), None)
        self.assertEqual(str(self.game), '40 - 40')

    def test_add_point(self):
        self.game.point1 = 0
        self.game.point2 = 0

        self.game.add_point(0)
        self.assertEqual(self.game.point1, 0)
        self.assertEqual(self.game.point2, 1)
        self.game.add_point(1)
        self.assertEqual(self.game.point1, 1)
