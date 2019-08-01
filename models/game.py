class Game:
    """single game"""

    _win_point = 4
    _point_displays = {0: "0", 1: "15", 2: "30", 3: "40"}

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
                return "Game" if self.point1 - self.point2 > 1 else "40*"
            else:
                return "40"

    @property
    def point2_display(self):
        if self.point2 in self._point_displays:
            return self._point_displays[self.point2]
        else:
            if self.point1 < self.point2:
                return "Game" if self.point2 - self.point1 > 1 else "40*"
            else:
                return "40"

    def __str__(self):
        return f"{self.point1_display} - {self.point2_display}"

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
            raise ValueError("player1_point should be number.")
        if player1_point:
            self.point1 += 1
        else:
            self.point2 += 1
        print(player1_point, ",", self)
        return self.get_winner()

    def get_player_point(self, player_name):
        """return player's win and lose, if not this game return 0,0"""
        if player_name == self.player1:
            return self.point1, self.point2
        elif player_name == self.player2:
            return self.point2, self.point1
        return 0, 0
