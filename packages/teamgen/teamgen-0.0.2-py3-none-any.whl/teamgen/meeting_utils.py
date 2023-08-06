import random
from typing import List
from .player import Player


def get_temp_list(g1: Player, g2: Player, balance=True):
    """

    :param g1:
    :param g2:
    :return:
    """

    t_g1 = g1.copy()
    t_g2 = g2.copy()

    if balance:
        t_g1, t_g2 = balance_groups(t_g1, t_g2)

    return t_g1, t_g2


def balance_groups(g1: List[Player], g2: List[Player]):

    d = len(g1) - len(g2)
    if d != 0:

        if d % 4 == 0:
            # We can work with this.
            # return t_men, t_women
            pass

        if d > 0:
            big, sm = g1, g2
        else:
            big, sm = g2, g1

        while d:
            p = random.choice(list(big))
            sm.append(p)
            big.remove(p)
            d = len(g1) - len(g2)
    return g1, g2

