import unittest
from models.game import Game
from models.set import Set
from models.match import Match


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
        self.assertEqual(self.game.get_player_point(self.game.player1), (0, 3))
        self.assertEqual(self.game.get_player_point(self.game.player2), (3, 0))

        self.game.point1 = 3
        self.game.point2 = 3
        self.assertEqual(self.game.get_winner(), None)
        self.assertEqual(str(self.game), '40 - 40')
        self.assertEqual(self.game.get_player_point(self.game.player1), (3, 3))
        self.assertEqual(self.game.get_player_point(self.game.player2), (3, 3))

        self.game.point1 = 4
        self.game.point2 = 3
        self.assertEqual(self.game.get_winner(), None)
        self.assertEqual(str(self.game), '40* - 40')
        self.assertEqual(self.game.get_player_point(self.game.player1), (4, 3))
        self.assertEqual(self.game.get_player_point(self.game.player2), (3, 4))

        self.game.point1 = 4
        self.game.point2 = 2
        self.assertEqual(self.game.get_winner(), self.game.player1)
        self.assertEqual(str(self.game), 'Game - 30')
        self.assertEqual(self.game.get_player_point(self.game.player1), (4, 2))
        self.assertEqual(self.game.get_player_point(self.game.player2), (2, 4))

        self.game.point1 = 4
        self.game.point2 = 5
        self.assertEqual(self.game.get_winner(), None)
        self.assertEqual(str(self.game), '40 - 40*')
        self.assertEqual(self.game.get_player_point(self.game.player1), (4, 5))
        self.assertEqual(self.game.get_player_point(self.game.player2), (5, 4))

        self.game.point1 = 4
        self.game.point2 = 6
        self.assertEqual(self.game.get_winner(), self.game.player2)
        self.assertEqual(str(self.game), '40 - Game')
        self.assertEqual(self.game.get_player_point(self.game.player1), (4, 6))
        self.assertEqual(self.game.get_player_point(self.game.player2), (6, 4))

        self.game.point1 = self.game.point2 = 6
        self.assertEqual(self.game.get_winner(), None)
        self.assertEqual(str(self.game), '40 - 40')
        self.assertEqual(self.game.get_player_point(self.game.player1), (6, 6))
        self.assertEqual(self.game.get_player_point(self.game.player2), (6, 6))

    def test_add_point(self):
        self.game.point1 = 0
        self.game.point2 = 0

        self.game.add_point(0)
        self.assertEqual(self.game.point1, 0)
        self.assertEqual(self.game.point2, 1)
        self.game.add_point(1)
        self.assertEqual(self.game.point1, 1)
