import logging
from typing import List
from .Team import Team

logger = logging.getLogger(__name__)


class Match:
    """
    Worst diff is a pair of 2.0's against a pair of 5.0's
        abs(10.0 - 4.0) or 6.0
    """
    diff_max = 6.0
    match_spread_factor = 1.0

    def __init__(self, t1: Team, t2: Team, factor=None):
        self.t1: Team = t1
        self.t2: Team = t2
        self._quality: float = None
        self._diff: float = None

        if factor is not None:
            self.match_spread_factor = factor

    def set_factor(self, factor):
        self.match_spread_factor = factor

    @property
    def teams(self):
        return [self.t1, self.t2]

    @property
    def enumerate(self):
        """ Return a data structure that makes it easy to set history """
        return [
            [self.t1.p1, self.t1.p2, self.t2.players],
            [self.t1.p2, self.t1.p1, self.t2.players],
            [self.t2.p1, self.t2.p2, self.t1.players],
            [self.t2.p2, self.t2.p1, self.t1.players],
        ]

    @property
    def diff(self):
        c1 = self.t1.combined_microntrp
        c2 = self.t2.combined_microntrp
        self._diff = round(abs(c1 - c2), 1)
        return self._diff

    @property
    def diff_quality(self):
        """ Quality of team play from 0 to 100 """
        diff = self.diff
        return 100 - 100 * (diff / self.diff_max)

    @property
    def quality(self):
        """
        Calculate a quality score
        100 is ideal, 0 is lowest

        q1 and q1 both range from 0 to 100
        diff
        :return:
        """
        # Calculate weights
        fteam1 = self.t1.team_factor
        fteam2 = self.t2.team_factor
        fspread = self.match_spread_factor

        total = fteam1 + fteam2 + fspread
        pct_team1 = fteam1 / total
        pct_team2 = fteam2 / total
        pct_spread = fspread / total

        Qd = self.diff_quality
        Q1 = self.t1.quality
        Q2 = self.t2.quality
        Q = (pct_team1 * Q1
             + pct_team2 * Q2
             + pct_spread * Qd)
        self._quality = Q
        return round(self._quality)

    def display(self):
        self.t1.display()
        logger.debug("Versus")
        self.t2.display()
        logger.debug(f"diff:{self.diff:4.2f} "
                     f"Quality:{self.quality:4.2f}\n")

    def __str__(self):
        return f"{self.t1} vs {self.t2} {self.diff:3.2f} {self.quality:3.1f}"

    def __repr__(self):
        return str(self)

    def todict(self):
        return {'t1': self.t1.todict(), 't2': self.t2.todict()}