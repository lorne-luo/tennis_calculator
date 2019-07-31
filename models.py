from collections import OrderedDict


class Game():
    """single game"""
    pass
class Set():
    """single set"""
    _win_game = 6
    _tiebreak_game = 7

    def __init__(self, match, set_number):
        self.set_number = set_number
        self.match = match
        self.current_game_number = None
        self.games = OrderedDict()

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
        if self.game_score1 >= self._win_game or self.game_score2 >= self._win_game:
            if self.game_score1 == self._tiebreak_game or self.game_score1 - self.game_score2 > 1:
                return self.player1
            elif self.game_score2 == self._tiebreak_game or self.game_score2 - self.game_score1 > 1:
                return self.player2

        return None  # not finished yet

    def get_game(self, next=True):
        """return current game, create next game automatically if next=True"""
        if self.current_game_number:
            # current game is on going
            return self.games[self.current_game_number]
        elif next:
            # get next game number
            self.current_game_number = max(self.games.keys()) + 1 if self.games else 1
            self.games[self.current_game_number] = Set(self, self.current_game_number)
            return self.games[self.current_game_number]
        else:
            return None



class Match():
    """single match"""

    _win_set = 2  # only women, best-of-three

    def __init__(self, match_number, player1, player2):
        self.match_number = match_number
        self.player1 = player1
        self.player2 = player2
        self.current_set_number = None
        self.sets = OrderedDict()

    @property
    def set_score1(self):
        return len(list(filter(lambda s: s.get_winner() == self.player1, self.sets.values())))

    @property
    def set_score2(self):
        return len(list(filter(lambda s: s.get_winner() == self.player2, self.sets.values())))

    def __str__(self):
        return f'{self.player1} vs {self.player1}: %s' % ', '.join([str(s) for s in self.sets])

    def get_set(self, next=True):
        """return current set, create next set automatically if next=True"""
        if self.current_set_number:
            # current set is on going
            return self.sets[self.current_set_number]
        elif next:
            # get next set number
            self.current_set_number = max(self.sets.keys()) + 1 if self.sets else 1
            self.sets[self.current_set_number] = Set(self, self.current_set_number)
            return self.sets[self.current_set_number]
        else:
            return None


    def get_winner(self):
        if self.set_score1 >= self._win_set:
            return self.player1
        elif self.set_score2 >= self._win_set:
            return self.player2
        return None  # not finished yet


class Tournament():
    """stand for whole tournament"""

    def __init__(self):
        self.matches = {}

    def create_match(self, match_number, player1, player2):
        try:
            match_number = int(match_number)
        except:
            raise ValueError('match_number should be number.')
        match_number = int(match_number)
        self.matches[match_number] = Match(match_number, player1, player2)
        return self.matches[match_number]

    def get_match(self, match_number):
        try:
            match_number = int(match_number)
        except:
            raise ValueError('match_number should be number.')
        return self.matches.get(match_number)

    @property
    def match_count(self):
        return len(self.matches)
