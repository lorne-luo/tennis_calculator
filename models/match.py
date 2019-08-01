from collections import OrderedDict

from models.set import Set


class Match:
    """single match"""

    _win_set = 2  # only women, best-of-three
    _best_of = 3

    def __init__(self, match_number, player1, player2):
        self.match_number = match_number
        self.player1 = player1
        self.player2 = player2
        self.current_set_number = None
        self.sets = OrderedDict()

    @property
    def set_score1(self):
        """player1's set score"""
        return len(
            list(filter(lambda s: s.get_winner() == self.player1, self.sets.values()))
        )

    @property
    def set_score2(self):
        """player2's set score"""
        return len(
            list(filter(lambda s: s.get_winner() == self.player2, self.sets.values()))
        )

    def __str__(self):
        return f"{self.player1} vs {self.player2}: %s" % ", ".join(
            [str(s) for s in self.sets.values()]
        )

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
            is_deciding_set = self.current_set_number == self._best_of
            self.sets[self.current_set_number] = Set(
                self, self.current_set_number, is_deciding_set
            )
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
        """return winner of this match, if not finished return None"""
        if self.set_score1 >= self._win_set:
            return self.player1
        elif self.set_score2 >= self._win_set:
            return self.player2
        return None  # not finished yet

    @property
    def set_count(self):
        return len(self.sets)

    def print(self):
        """print the match result to console"""
        winner = self.get_winner()
        swap_position = winner != self.player1
        if not winner:
            print("This match is still on ongoing.")
        else:
            if swap_position:
                print(f"{self.player2} defeated {self.player1}")
            else:
                print(f"{self.player1} defeated {self.player2}")

        if swap_position:
            print(f"{self.set_score2} sets to {self.set_score1}")
        else:
            print(f"{self.set_score1} sets to {self.set_score2}")

        for _set in self.sets.values():
            if swap_position:
                print(f"{_set.game_score2} {_set.game_score1}")
            else:
                print(f"{_set.set_score1} {_set.set_score2}")

    def get_player_point(self, player_name):
        """return player's win and lose, if not this game return 0,0"""

        total_win = total_lose = 0
        for _set in self.sets.values():
            if player_name == self.player1:
                win, lose = _set.get_player_point(self.player1)
            elif player_name == self.player2:
                win, lose = _set.get_player_point(self.player2)
            else:
                return 0, 0
            total_win += win
            total_lose += lose

        return total_win, total_lose
