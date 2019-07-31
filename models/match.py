from collections import OrderedDict

from models.set import Set


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
        return f'{self.player1} vs {self.player2}: %s' % ', '.join([str(s) for s in self.sets.values()])

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
            return None
        winner = _set.add_point(player1_point)
        if winner:
            self.current_set_number = None
        return self.get_winner()

    def get_winner(self):
        if self.set_score1 >= self._win_set:
            return self.player1
        elif self.set_score2 >= self._win_set:
            return self.player2
        return None  # not finished yet

    @property
    def set_count(self):
        return len(self.sets)
