from models.match import Match


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

    def get_player_point(self, player_name):
        """get player's win and lose"""
        win_lose_points = [match.get_player_point(player_name) for match in self.matches.values() if
                           player_name in [match.player1, match.player2]]
        # sumup win and lose
        win_point = sum([match[0] for match in win_lose_points])
        lose_point = sum([match[1] for match in win_lose_points])

        return win_point, lose_point
