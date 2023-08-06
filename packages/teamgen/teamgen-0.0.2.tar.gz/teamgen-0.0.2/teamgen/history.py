from typing import List
from .player import Player


class HistoryBase:
    """ Base class for meeting history """

    def __init__(self, see_player_once=False):
        self._see_player_once = see_player_once

    def restart(self):
        raise NotImplemented('Must implement this method!')

    def add_round(self, round):
        raise NotImplemented('Must implement this method!')

    def get_valid_partner(self,
                          player: Player,
                          others: List[Player],
                          available: List[Player]) -> Player:
        raise NotImplemented('Must implement this method!')

    def get_valid_opponent(self, player, opponents) -> Player:
        raise NotImplemented('Must implement this method!')

    def limit_partner_differences(self, player, available):
        """ Limit how many 'low' players a high player plays with """
        return available

    @property
    def see_player_once(self):
        return self._see_player_once

    @see_player_once.setter
    def see_player_once(self, value):
        self._see_player_once = value
