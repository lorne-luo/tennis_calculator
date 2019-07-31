class Set():
    pass


class Match():
    pass


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
