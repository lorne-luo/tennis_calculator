from collections import OrderedDict

from models.game import Game


class Set():
    """single set"""
    _win_game = 6
    _tiebreak_game = 7

    def __init__(self, match, set_number, is_deciding=False):
        self.set_number = set_number
        self.match = match
        self.current_game_number = None
        self.games = OrderedDict()
        self.is_deciding = is_deciding

    @property
    def game_score1(self):
        return len(list(filter(lambda s: s.get_winner() == self.player1, self.games.values())))

    @property
    def game_score2(self):
        return len(list(filter(lambda s: s.get_winner() == self.player2, self.games.values())))

    def __str__(self):
        return f'{self.game_score1} - {self.game_score2}'

    @property
    def player1(self):
        return self.match.player1

    @property
    def player2(self):
        return self.match.player2

    def get_winner(self):
        if self.is_deciding:
            # for deciding set, must lead 2 set
            if self.game_score1 >= 6 or self.game_score2 >= 6:
                if self.game_score1 - self.game_score2 > 1:
                    return self.player1
                elif self.game_score2 - self.game_score1 > 1:
                    return self.player2
        else:
            if self.game_score1 >= self._win_game or self.game_score2 >= self._win_game:
                if self.game_score1 == self._tiebreak_game or self.game_score1 - self.game_score2 > 1:
                    return self.player1
                elif self.game_score2 == self._tiebreak_game or self.game_score2 - self.game_score1 > 1:
                    return self.player2

        return None  # not finished yet

    def get_game(self, game_number):
        if game_number in self.games:
            return self.games[game_number]
        return None

    def create_or_get_game(self, next=True):
        """return current game, create next game automatically if next=True"""
        if self.current_game_number:
            # current game is on going
            return self.games[self.current_game_number]
        elif next:
            # get next game number
            self.current_game_number = max(self.games.keys()) + 1 if self.games else 1
            self.games[self.current_game_number] = Game(self.current_game_number, self)
            return self.games[self.current_game_number]
        else:
            return None

    def add_point(self, player1_point):
        """add player1's point to this set"""
        game = self.create_or_get_game()
        if not game:
            return None

        winner = game.add_point(player1_point)
        if winner:
            self.current_game_number = None
        return self.get_winner()

    def get_player_point(self, player_name):
        """return player's win and lose, if not this game return 0,0"""
        total_win = total_lose = 0
        for game in self.games.values():
            if player_name == self.player1:
                win, lose = game.get_player_point(self.player1)
            elif player_name == self.player2:
                win, lose = game.get_player_point(self.player2)
            else:
                return 0, 0
            total_win += win
            total_lose += lose

        return total_win, total_lose
