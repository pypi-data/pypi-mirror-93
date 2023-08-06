import logging
from typing import List
import math
import itertools

logger = logging.getLogger(__name__)


class RoundStats:
    def __init__(self):

        self._diff_history = []
        self._q_history = []

    def push_histories(self, diff=None, q=None):
        if diff: self._diff_history.append(diff)
        if q: self._q_history.append(q)

    @property
    def diff_history(self):
        return self._diff_history or [-1]

    @property
    def q_history(self):
        return self._q_history or [-1]

    def get_stats(self):
        max_diff = 0.0
        min_diff = 1000.0

        maxq = 100.0
        minq = -1.0

        dh = self._diff_history
        qh = self._q_history
        if dh:
            max_diff = max(dh)
            min_diff = min(dh)
        if qh:
            maxq = max(qh)
            minq = min(qh)

        return max_diff, min_diff, minq, maxq

    @property
    def min_diff(self):
        if self._diff_history:
            return min(self._diff_history)
        return 1000

    @property
    def max_q(self):
        if self._q_history:
            return max(self._q_history)

    @property
    def min_q(self):
        if self._q_history:
            return min(self._q_history)

    @staticmethod
    def print_check_stats():
        print('')

    def __str__(self):
        return " ".join([str(m) for m in self.matches])

    def __repr__(self):
        return str(self)
