import logging
from typing import List
import math

from .Match import Match

logger = logging.getLogger(__name__)


class MatchRound:
    def __init__(self, matches=None):
        self.matches: List[Match] = []
        if matches:
            self.matches = matches

        self._diff_history = []
        self._q_history = []

    def clone(self):
        s = MatchRound(self.matches)
        return s

    def add_match(self, match: Match):
        self.matches.append(match)

    def push_histories(self, diff=None, q=None):
        if diff: self._diff_history.append(diff)
        if q: self._q_history.append(q)

    @property
    def diff_history(self):
        return self._diff_history or [-1]

    @property
    def q_history(self):
        return self._q_history or [-1]

    @property
    def diffs(self):
        """
        Take all diff values, put them in a list.

        Return the sorted list.. later, I'll write a comparison
        algorithm.

        Return the max diff value, the worst match, and then
        the second max value, i.e. the 2nd worst match. This
        would allow me to prefer a set that has 3 great matches
        and one bad one, over a set that has potentially 4 bad matches..

        Consider two cases:
          0.5,0.6,0.5,0.6

          0.1,0.0,0.2,0.6

        In the previous algorithm, they are the same... here, the second
        one could be preferred.

        """
        diffs = []
        for m in self.matches:
            diffs.append(m.diff)

        diffs.sort()

        return diffs

    @property
    def qualities(self):
        return [
            m.quality
            for m in self.matches
        ]

    @property
    def quality_average(self):
        Q = self.qualities
        return round(sum(Q)/len(Q))

    @property
    def quality_min(self):
        return min(self.qualities)

    @property
    def quality_max(self):
        return max(self.qualities)

    def diff_stats(self):
        diffs = [m.diff for m in self.matches]
        # qvals = [m.quality() for m in self.matches]
        diffs.sort()
        return max(diffs), sum(diffs) / len(diffs), diffs

    def display(self):
        for match in self.matches:
            match.display()

    def show_diffs(self):
        diffs = ["%4.2f" % match.diff for match in self.matches]
        logger.debug("Diffs: " + "\t".join(diffs))

    def __str__(self):
        return " ".join([str(m) for m in self.matches])

    def __repr__(self):
        return str(self)

    def todict(self):
        dval = [
            m.todict() for m in self.matches
        ]
        return dval