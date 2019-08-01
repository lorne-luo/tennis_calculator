import unittest
from collections import OrderedDict
from unittest import mock

from models.match import Match


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

    @mock.patch("models.match.Match.set_score1", mock.PropertyMock(return_value=0))
    @mock.patch("models.match.Match.set_score2", mock.PropertyMock(return_value=2))
    def test_get_winner1(self):
        self.assertEqual(self.match.get_winner(), self.match.player2)

    @mock.patch("models.match.Match.set_score1", mock.PropertyMock(return_value=2))
    @mock.patch("models.match.Match.set_score2", mock.PropertyMock(return_value=1))
    def test_get_winner2(self):
        self.assertEqual(self.match.get_winner(), self.match.player1)

    @mock.patch("models.match.Match.set_score1", mock.PropertyMock(return_value=1))
    @mock.patch("models.match.Match.set_score2", mock.PropertyMock(return_value=1))
    def test_get_winner3(self):
        self.assertEqual(self.match.get_winner(), None)

    def test_add_point(self):
        self.match.add_point(1)
        self.assertEqual(self.match.create_or_get_set().create_or_get_game().point1, 1)
        self.assertEqual(self.match.create_or_get_set().create_or_get_game().point2, 0)
        self.assertEqual(self.match.get_player_point(self.match.player1), (1, 0))
        self.assertEqual(self.match.get_player_point(self.match.player2), (0, 1))

        # win first game
        self.match.add_point(1)
        self.assertEqual(self.match.get_player_point(self.match.player1), (2, 0))
        self.assertEqual(self.match.get_player_point(self.match.player2), (0, 2))

        self.match.add_point(1)
        self.assertEqual(self.match.get_player_point(self.match.player1), (3, 0))
        self.assertEqual(self.match.get_player_point(self.match.player2), (0, 3))

        winner = self.match.add_point(1)
        self.assertEqual(self.match.get_player_point(self.match.player1), (4, 0))
        self.assertEqual(self.match.get_player_point(self.match.player2), (0, 4))
        self.assertEqual(winner, None)  # only win 1 game, not win set yet
        self.assertEqual(self.match.get_set(1).game_score1, 1)
        self.assertEqual(str(self.match.get_set(1)), '1 - 0')
