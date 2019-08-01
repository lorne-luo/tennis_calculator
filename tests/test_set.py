import unittest
from unittest import mock

from models.set import Set
from models.match import Match


class SetTestCase(unittest.TestCase):
    set = Set(Match(1, "Player A", "Player B"), 1)

    def test_property(self):
        self.assertEqual(self.set.player1, "Player A")
        self.assertEqual(self.set.player2, "Player B")
        self.assertEqual(self.set.get_winner(), None)
        self.assertEqual(self.set.get_game(11), None)

    @mock.patch("models.set.Set.game_score1", mock.PropertyMock(return_value=0))
    @mock.patch("models.set.Set.game_score2", mock.PropertyMock(return_value=6))
    def test_get_winner1(self):
        self.assertEqual(self.set.get_winner(), self.set.player2)

    @mock.patch("models.set.Set.game_score1", mock.PropertyMock(return_value=7))
    @mock.patch("models.set.Set.game_score2", mock.PropertyMock(return_value=6))
    def test_get_winner2(self):
        self.assertEqual(self.set.get_winner(), self.set.player1)

    @mock.patch("models.set.Set.game_score1", mock.PropertyMock(return_value=4))
    @mock.patch("models.set.Set.game_score2", mock.PropertyMock(return_value=6))
    def test_get_winner3(self):
        self.assertEqual(self.set.get_winner(), self.set.player2)

    @mock.patch("models.set.Set.game_score1", mock.PropertyMock(return_value=5))
    @mock.patch("models.set.Set.game_score2", mock.PropertyMock(return_value=6))
    def test_get_winner4(self):
        self.assertEqual(self.set.get_winner(), None)

    def test_create_game(self):
        self.assertEqual(self.set.current_game_number, None)  # game not start yet
        self.assertFalse(self.set.create_or_get_game(next=False))
        current_game = self.set.create_or_get_game()
        self.assertTrue(current_game)

    def test_add_point(self):
        self.set.add_point(1)
        self.assertEqual(self.set.get_player_point(self.set.player1), (1, 0))
        self.assertEqual(self.set.get_player_point(self.set.player2), (0, 1))
        self.assertEqual(self.set.create_or_get_game().point1, 1)
        self.assertEqual(self.set.create_or_get_game().point2, 0)

        self.set.add_point(1)
        self.assertEqual(self.set.get_player_point(self.set.player1), (2, 0))
        self.assertEqual(self.set.get_player_point(self.set.player2), (0, 2))
        self.set.add_point(1)
        self.assertEqual(self.set.get_player_point(self.set.player1), (3, 0))
        self.assertEqual(self.set.get_player_point(self.set.player2), (0, 3))

        # win first game
        winner = self.set.add_point(1)
        self.assertEqual(winner, None)  # only win 1 game, not win set yet
        self.assertEqual(self.set.game_score1, 1)
        self.assertEqual(str(self.set), "1 - 0")
