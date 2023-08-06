class NoValidOpponent(Exception):

    def __init__(self, player=None):
        self.message = "No valid opponent found"
        if player:
            self.message = "No valid opponent for {player}"


class NoValidPartner(Exception):
    pass