import logging
from .player import Player

logger = logging.getLogger(__name__)


class Team:
    """
    Represents a pair of players on a team.

    max_diff is the maximum variation we would expect,
    so a 2.0 with a 5.0
    """
    team_factor = 1.0
    max_diff = 3.0

    def __init__(self, player1=None, player2=None, factor=None):
        self.p1: Player = player1
        self.p2: Player = player2
        if factor is not None:
            self.team_factor = factor

    def set_factor(self, factor):
        self.team_factor = factor

    @property
    def players(self):
        return [self.p1, self.p2]

    @property
    def combined_microntrp(self):
        """
        Expecting a mixed team.
        If there are 2 ladies, i.e. we were short a guy, then make a slight
        reduction in combined to compensate

        If this is 2 men, then make a slight increase.

        """
        # if self.p1.gender == 'F' and self.p1.gender == 'F':
        #     combined = 0.92 * self.p1.microntrp + self.p2.microntrp
        # elif self.p1.gender == 'M' and self.p1.gender == 'M':
        #     combined = 1.08 * (self.p1.microntrp + self.p2.microntrp)
        # else:
        if self.p1 and self.p2:
            combined = self.p1.microntrp + self.p2.microntrp
            return combined
        elif self.p1:
            return self.p1.microntrp
        elif self.p2:
            return self.p2.microntrp

        return 0.0

    @property
    def spread(self):
        if self.p1 and self.p2:
            return abs(self.p1.microntrp - self.p2.microntrp)
        elif self.p1:
            return self.p1.microntrp
        elif self.p2:
            return self.p2.microntrp
        return 0

    @property
    def quality(self):
        """ Range from 100 as best, to zero as worst we calculate """
        diff = min(self.max_diff, self.team_factor * abs(self.p1.microntrp - self.p2.microntrp))
        Q = round(100 - 100 * (diff / self.max_diff))
        return Q

    def display(self):
        p1 = self.p1
        p2 = self.p2
        logger.info(
            f"{p1 and p1.name} {p1 and p1.ntrp:3.2f}/"
            f"{p1 and p1.microntrp:3.2f}"
            f" and "
            f"{p2 and p2.name} {p2 and p2.ntrp:3.2f}/"
            f"{p2 and p2.microntrp:3.2f}"
            f" = {p1 and p2 and self.combined_microntrp:3.2f}")

    def __str__(self):
        name1 = ''
        name2 = '---'
        un1 = 0.0
        un2 = 0.0
        if self.p1:
            name1 = self.p1.name
            un1 = self.p1.microntrp

        if self.p2:
            name2 = self.p2.name
            un2 = self.p2.microntrp

        return (f"{name1} and {name2}"
                f" @ {un1 + un2:3.2f} {un1}/{un2}")

    def __repr__(self):
        str(self)

    def todict(self):
        return {'p1': self.p1.todict(), "p2": self.p2.todict() }

