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
        self.assertEqual(str(match2), 0)


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
        self.match.add_point(1)
        self.assertEqual(self.match.create_or_get_set().create_or_get_game().point1, 1)
        self.assertEqual(self.match.create_or_get_set().create_or_get_game().point2, 0)

        # win first game
        self.match.add_point(1)
        self.match.add_point(1)
        winner = self.match.add_point(1)
        self.assertEqual(winner, None)  # only win 1 game, not win set yet
        self.assertEqual(self.match.get_set(1).game_score1, 1)
        self.assertEqual(str(self.match.get_set(1)), '1 - 0')


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
        self.set.add_point(1)
        self.assertEqual(self.set.create_or_get_game().point1, 1)
        self.assertEqual(self.set.create_or_get_game().point2, 0)

        # win first game
        self.set.add_point(1)
        self.set.add_point(1)
        winner = self.set.add_point(1)
        self.assertEqual(winner, None)  # only win 1 game, not win set yet
        self.assertEqual(self.set.game_score1, 1)
        self.assertEqual(str(self.set), '1 - 0')


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
