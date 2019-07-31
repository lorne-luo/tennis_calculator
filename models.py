from collections import OrderedDict


class Game():
    """single game"""
    _win_point = 4
    _point_displays = {
        0: '0',
        1: '15',
        2: '30',
        3: '40',
    }

    def __init__(self, game_number, set):
        self.game_number = game_number
        self.set = set
        self.point1 = 0
        self.point2 = 0

    @property
    def player1(self):
        return self.set.match.player1

    @property
    def player2(self):
        return self.set.match.player2

    @property
    def point1_display(self):
        if self.point1 in self._point_displays:
            return self._point_displays[self.point1]
        else:
            if self.point1 > self.point2:
                return 'Game' if self.point1 - self.point2 > 1 else '40*'
            else:
                return '40'

    @property
    def point2_display(self):
        if self.point2 in self._point_displays:
            return self._point_displays[self.point2]
        else:
            if self.point1 < self.point2:
                return 'Game' if self.point2 - self.point1 > 1 else '40*'
            else:
                return '40'

    def __str__(self):
        return f'{self.point1_display} - {self.point2_display}'

    def get_winner(self):
        if self.point1 >= self._win_point or self.point2 >= self._win_point:
            if self.point1 - self.point2 > 1:
                return self.player1
            if self.point2 - self.point1 > 1:
                return self.player2
        return None

    def add_point(self, player1_point):
        """add player1's point to this match"""
        try:
            player1_point = int(player1_point)
        except:
            raise ValueError('player1_point should be number.')
        if player1_point:
            self.point1 += 1
        else:
            self.point2 += 1

        return self.get_winner()


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
            return

        winner = game.add_point(player1_point)
        if winner:
            self.current_game_number = None
        return winner


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
        """player1's set score"""
        return len(list(filter(lambda s: s.get_winner() == self.player1, self.sets.values())))

    @property
    def set_score2(self):
        """player2's set score"""
        return len(list(filter(lambda s: s.get_winner() == self.player2, self.sets.values())))

    def __str__(self):
        return f'{self.player1} vs {self.player1}: %s' % ', '.join([str(s) for s in self.sets])

    def get_set(self, set_number):
        if set_number in self.sets:
            return self.sets[set_number]
        return None

    def create_or_get_set(self, next=True):
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

    def add_point(self, player1_point):
        """add player1's point to this match"""
        _set = self.create_or_get_set()
        if not _set:
            return
        winner = _set.add_point(player1_point)
        if winner:
            self.current_set_number = None
        return winner

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
