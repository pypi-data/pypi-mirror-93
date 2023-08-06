from typing import List
from .round import MatchRound
from .history import HistoryBase
from .random_builder import BuilderBase


class Meeting:
    def __init__(self, n_courts, n_sets, men, women,
                 history: HistoryBase = None,
                 builder: BuilderBase = None,
                 ):
        self.rounds: List[MatchRound] = []
        self.history = history
        self.builder = builder
        self._see_player_once = False

    def restart(self):
        self.rounds = []
        self.history.restart()
        self.builder.restart()

    def add_round(self, new_round):
        self.rounds.append(new_round)
        self.history.add_round(new_round)

    def round_count(self):
        return len(self.rounds)

    def get_rounds(self):
        return self.rounds

    def get_new_round(self, diff_max=0.6, quality_min=90, max_tries=50):
        return self.builder.get_new_round(
            diff_max=diff_max,
            quality_min=quality_min, max_tries=max_tries
        )

    def print_check_stats(self):
        self.builder.print_check_stats()

    @property
    def see_player_once(self):
        return self.history.see_player_once

    @see_player_once.setter
    def see_player_once(self, value):
        self.history.see_player_once = value

    @property
    def max_iterations(self):
        return self.builder.max_iterations

    @max_iterations.setter
    def max_iterations(self, value):
        self.builder.max_iterations = value

    @property
    def round_count(self):
        return len(self.rounds)

