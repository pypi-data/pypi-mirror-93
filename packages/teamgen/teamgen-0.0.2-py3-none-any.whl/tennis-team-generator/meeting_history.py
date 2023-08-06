import logging
import random
from typing import List
import itertools
from collections import Counter, defaultdict
from .exceptions import NoValidOpponent, NoValidPartner

from .Match import Match
from .Team import Team
from .round import MatchRound
from .stats import RoundStats
from .player import Player
from .history import HistoryBase

logger = logging.getLogger(__name__)


def make_key(m, f):
    return "%s %s:%s %s" % (m.first, m.last, f.first, f.last)


def make_sorted_key(a, b):
    if a.pid < b.pid:
        return make_key(a, b)
    else:
        return make_key(b, a)


class MeetingHistory(HistoryBase):
    def __init__(self, group1, group2,
                 see_player_once=False,
                 low_threshold=0.75):

        super().__init__(see_player_once=see_player_once)

        self.low_threshold = low_threshold

        self.group1 = group1
        self.group2 = group2

        self.Opponents = {}
        self.Partners = {}
        self.Seen = defaultdict(Counter)
        self.Opposites = {}
        self.InvalidOpponents = {}
        self.InvalidPartners = {}

        # Should do this only once
        random.seed()
        self.restart()

    def restart(self):
        """
        Clear all statistics and restart the checking
        """

        self.Partners = {}
        self.Opponents = {}
        self.Opposites = {}
        for p in self.group1 + self.group2:
            bad_match = []
            if p.pk == 87:
                bad_match = [p for p in self.group2 if p.pk==71]
            self.Partners[p] = set()
            self.Opposites[p] = Counter()
            self.Opponents[p] = set()
            self.InvalidOpponents[p] = set(bad_match)
            self.InvalidPartners[p] = set(bad_match)

        for p in self.group1:
            if p.pk == 87:  # Curtis
                for pp in self.group2:
                    if pp.pk == 71:
                        self.InvalidPartners[p].update([pp])
                        self.InvalidOpponents[p].update([pp])
                        self.InvalidPartners[pp].update([p])
                        self.InvalidOpponents[pp].update([p])

    def special_partner_rules(self, *, player: Player,
                              opponents: List[Player],
                              available: List[Player],
                              parnter: Player = None) -> Player:
        """ Apply any special rules for a partner """

        pass

    def add_round(self, round):
        """
        Add the round to the history

        """
        for match in round.matches:

            for player, partner, opponents in match.enumerate:
                self.Partners[player].update([partner])
                self.Opponents[player].update(opponents)
                self.Seen[player].update([partner, *opponents])

        self.update_invalids()

    def update_invalids(self):
        """
        Iterate of the  men and update the invalid partner or opposite sex
        opponent for each
        :return:
        """
        for player in [*self.group1, *self.group2]:
            self.update_invalids_for_player(player)

    def update_invalids_for_player(self, player):
        """
        Mark players as invalid partners or invalid opponents if
        a player has seen them more than "max" times.

        Max times could be 1 for larger groups, or 2 for smaller groups.
        With 3 courts, a value of 1 does not work well.

        :param player:
        :return:
        """
        seen = self.Seen[player]

        max_count = 1 if self.see_player_once else 2

        seen_max_count_times = set([p for p in seen if seen[p] >= max_count])
        if seen_max_count_times:
            self.InvalidOpponents[player].update(seen_max_count_times)
            self.InvalidPartners[player].update(seen_max_count_times)

    def limit_partner_differences(self, player, available):
        """
        Implement a partner difference limit. This keeps a high player
        from playing with multiple low players in a night

        :param player:
        :param available:
        :return:
        """
        previous_partners = self.Partners[player]

        # Eliminate partners with high diff-max
        available.difference_update(set([
            p for p in available if player.microntrp - p.microntrp > self.low_threshold
        ]))


        diff_max = None
        if previous_partners:
            max_diff = max([player.microntrp - p.microntrp
                            for p in previous_partners])
            if max_diff > self.low_threshold:
                # Limit to closer players from now on..
                diff_max = self.low_threshold

        # Remove any players with a diff > diff_max
        if diff_max is not None:
            available.difference_update(set([
                p for p in available if player.microntrp - p.microntrp > diff_max
            ]))

        return available

    def get_valid_opponent(self, player, opponents) -> Player:
        """
        The difference line retrieves a list of same-sex players that have
        not been opponents to this player yet.

        Implements the rule that men only play against other men
        once, and women only play against other women once.

        """

        remaining = opponents.copy()
        remaining.difference_update(self.Opponents[player])
        remaining.difference_update(self.InvalidOpponents[player])

        if not remaining:
            raise NoValidOpponent(player=player)

        opponent = random.choice(list(remaining))
        return opponent

    def get_valid_partner(self, *, player: Player,
                          opponents: List[Player],
                          available: List[Player],
                          partner: Player = None,
                          ) -> Player:
        """
        Player is the person we are picking a partner for.

        Players is a list of other players, to remove duplicates on court.

        Available is the list of Players available to be a partner

        The rule is -
        If a player has played with AND against m2, they are not a valid opponent
        M2 will have seen them 3 times.
        Also if they have played against M2 2x already, they can't play against them again.

        f1 is set to the first player in the current group if this is the second call.
        """

        invalid = [player, *opponents]
        if partner:
            invalid.append(partner)

        remaining = available.copy()
        remaining.difference_update(invalid)
        remaining.difference_update(self.InvalidPartners[player])

        # Can't partner with someone more than once
        remaining.difference_update(self.Partners[player])

        # Remove people that are invalid opponents of the others
        for p in opponents:
            remaining.difference_update(self.InvalidOpponents[p])

        remaining = self.limit_partner_differences(player, remaining)

        if not remaining:
            raise NoValidPartner()

        partner = random.choice(list(remaining))
        return partner

