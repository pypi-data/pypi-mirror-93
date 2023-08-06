import logging
import random
import copy
from typing import List
import itertools
from collections import Counter, defaultdict
from .exceptions import NoValidOpponent, NoValidPartner

from .Match import Match
from .Team import Team
from .round import MatchRound
from .stats import RoundStats
from .builder import BuilderBase
from .player import Player
from .meeting_history import MeetingHistory

from .meeting_utils import get_temp_list

logger = logging.getLogger(__name__)


def make_key(m, f):
    return "%s %s:%s %s" % (m.first, m.last, f.first, f.last)


def make_sorted_key(a, b):
    if a.pid < b.pid:
        return make_key(a, b)
    else:
        return make_key(b, a)


class RandomMeetingBuilder(BuilderBase):
    def __init__(self, n_courts, n_sets, men, women, history=None):
        self.men = men
        self.women = women
        self.all = men + women

        self.history: MeetingHistory = None

        if history is None:
            self.history = MeetingHistory()
        else:
            self.history = history

        self._ncourts = n_courts

        self._max_iterations = 100
        self.n_fails_by_invalid_partner = 0
        self.n_fails_by_diff = 0

        self.stats = RoundStats()
        self.diff_history = []
        self.q_history = []

        self._see_player_once = False

        self.chkMatchups = 0
        self.chkH2H = 0
        self.chkPairs = 0

        self.log_level = 0

        # Should do this only once
        random.seed()

    @property
    def max_iterations(self):
        return self._max_iterations

    @max_iterations.setter
    def max_iterations(self, n):
        self._max_iterations = n

    def restart(self):
        """
        Clear all statistics and restart the checking
        """
        self.history.restart()

    def get_new_round(self, diff_max=1.0,
                      quality_min=90,
                      max_tries=20,
                      special_requests=None):
        """
        This one needs to use the existing sets and list and pick a new
        randomization of the available sets.
        """

        """
        - Pick a guy
            - Pick an opponent from list of available opponents - men 
            not played yet
            - Pick two women from list of available women 
            (checking opposites, pairs)
        - From remaining guys, repeat the above.. and then for the last 
        set
        """
        tries = 0
        round = None

        max_build_tries = self.max_iterations

        while not round and tries < max_tries:
            logger.debug(f'Build round try={tries}')
            round = self.build_round(max_build_tries, diff_max, quality_min)
            tries += 1

            max_diff, min_diff, minq, maxq = self.stats.get_stats()

            logger.debug(
                f"Build round try DiffMax:{diff_max:5.3}({min_diff:5.3})"
                f" MinQ:{quality_min:5.1f}({minq:5.1f}, {maxq:5.1f}) Try:{tries}.")

        return round, self.stats

    def build_round(self, max_build_tries, diff_max, quality_min) -> MatchRound:
        """
        First, build a set of matches with men only.
        Next, add in the women. The men are assigned
        randomly, so it should not matter what the women
        are assigned as later.. they will be assigned
        randomly to the men.
        """

        diff = len(self.men) - len(self.women)
        if diff % 2:
            raise Exception("We have an odd number of players!")

        if diff == 0 or diff % 4 != 0:
            return self.build_balanced_round(max_build_tries, diff_max, quality_min)

        if diff > 0:
            g1 = self.men
            g2 = self.women
        else:
            g1 = self.women
            g2 = self.men

        return self.build_unbalanced_round(max_build_tries,
                                           diff_max,
                                           quality_min,
                                           g1, g2)

    def build_unbalanced_round(self,
                               max_build_tries,
                               diff_max,
                               quality_min,
                               g1, g2):
        """
        Build an unbalanced mixed group, with 1 or more courts of men's, or womens's and
        the remaining as mixed.

        g1 is to be the large of the two sets
        """

        assert (len(g1) > len(g2))
        diff = len(g1) - len(g2)

        n_tries = 0

        while n_tries < max_build_tries:
            logger.debug(f"Build iteration {n_tries}")

            t1, t2 = get_temp_list(g1, g2, balance=False)

            if abs(diff) == 4:
                """ Hard code this for now... """
                set1 = set(t1)
                set2 = set(t2)
                set1a = set(random.sample(set1, k=4))
                set1b = set1.copy()
                set1b -= set1a
                assert (len(set2) == len(set1b))

                try:
                    round1, set1a_partners = self.pick_first_group(set1a, courts=1)
                    round2, set1b_partners = self.pick_first_group(set1b, courts=3)
                except NoValidOpponent:
                    continue

                self.clear_check_stats()

                try:
                    if all([
                        self.add_partners(round1, set1a_partners,
                                          diff_max, quality_min,
                                          max_build_tries),
                        self.add_partners(round2, set2,
                                          diff_max, quality_min,
                                          max_build_tries),
                    ]):
                        return MatchRound(matches=[*round1.matches, *round2.matches])
                    self.print_check_stats()

                except NoValidPartner:
                    # we can continue on here, regenerate the men matchups
                    self.n_fails_by_invalid_partner += 1
                    pass
            n_tries = n_tries + 1

        return None

    """
    ToDo: Refactor the group code to be generic
    
    I should be able to pass in 2 groups, and then build the rounds from these
    two groups. This works for men's, women's or mixed.
    For men's and women's: Divide the group into equal parts, and pass them in a g1, and g2
    For mixed, pass in two groups, where g1 and g2 are men/women or women/men.
    In all cases, the groups are equal.
    
    A 2nd I can also take a group and split them into sub-groups, so if I have 8 men and 8 women:
      1) pull our 4 men and 4 women, split those into equal groups of 2 for each, and the rest (4/4) are
         spread across a pair of mixed courts.
     
    """

    def build_balanced_round(self, max_build_tries,
                             diff_max, quality_min,
                             ):
        """
        Build a round with equal numbers of men and women.
        g1 and g2 should have the same # of people in them.
        """

        n_tries = 0

        while n_tries < max_build_tries:
            t_g1, t_g2 = get_temp_list(self.men, self.women)

            # Build sets of men first.
            # If there is an exception thrown, then just ignore
            # it and try again..
            round, remainder = self.pick_first_group(t_g1)

            self.clear_check_stats()

            try:
                if self.add_partners(round, t_g2,
                                     diff_max, quality_min,
                                     max_build_tries):
                    return round
                self.print_check_stats()
            except NoValidPartner:
                # we can continue on here, regenerate the men matchups
                pass
            n_tries = n_tries + 1

        return None

    def add_partners(self,
                     round: MatchRound,
                     partners: List[Player],
                     diff_max: int, quality_min: int, num_tries: int) -> bool:
        """
        Upon entry, round will be a set that contains
        the initial partner, but with no 2nd partner entered. The
        initial player pairings will have been done randomly, so
        they should be okay.
        """
        curr_diff = diff_max + 1.0
        curr_q = 100.0
        min_diff = 1000.0
        max_q = 0

        passed_criteria = False

        best_round = None

        while num_tries and not passed_criteria:
            available = set(partners)

            for m in round.matches:
                player1 = m.t1.p1
                player2 = m.t2.p1

                available.difference_update([player1, player2])

                partner1 = self.history.get_valid_partner(
                    player=player1,
                    opponents=[player2],
                    available=available)
                available.remove(partner1)

                partner2 = self.history.get_valid_partner(
                    player=player2,
                    opponents=[player1, partner1],
                    available=available)
                available.remove(partner2)

                m.t1.p2 = partner1
                m.t2.p2 = partner2

            diffs = round.diffs
            if best_round is None:
                best_round = copy.deepcopy(round)

            # We want the worst case values here.
            curr_diff = max(diffs)
            curr_q = round.quality_min

            if curr_diff < max(best_round.diffs) and curr_q > best_round.quality_min:
                best_round = copy.deepcopy(round)

            min_diff = min(min_diff, curr_diff)
            max_q = max(max_q, round.quality_max)

            passed_criteria = (curr_diff <= diff_max and curr_q >= quality_min)
            #if not passed_criteria:
            #    logger.info(f"Failed: {curr_diff} <= {diff_max} {curr_q} >= {quality_min}")
            num_tries -= 1

        round.push_histories(min_diff, max_q)
        self.stats.push_histories(min_diff, max_q)

        if not passed_criteria:
            self.n_fails_by_diff += 1
        return passed_criteria

    def pick_first_group(self, players, courts=None):
        """
        Build a new set with a list of players from the first group.
        The first group may be men or women, depends on which set is
        larger.

        Each time this function is called, a new random set of players should be chosen.
        The only history used is the history of players that have played against each other
        this night. The get_valid_opponent function is used for this determination.
        """
        random.seed()

        invalid_retries = 10

        if courts is None:
            courts = self._ncourts

        while True:
            round = MatchRound()
            pset = set(players)
            try:
                for n in range(0, courts):
                    player_one = random.choice(list(pset))
                    pset.remove(player_one)
                    player_two = self.history.get_valid_opponent(player_one, pset)
                    pset.remove(player_two)
                    m = Match(Team(player_one),
                              Team(player_two))
                    round.add_match(m)
                return round, pset
            except NoValidOpponent as e:
                invalid_retries -= 1
                if invalid_retries is 0:
                    logger.debug('**************** Re-raising this issue **********')
                    raise NoValidOpponent(player=player_one)
                round = MatchRound()
                pset = set(players)

    def clear_check_stats(self):
        self.n_fails_by_invalid_partner = 0
        self.n_fails_by_diff = 0

    def print_check_stats(self):
        logger.debug(f"Failed Stats: Partner:{self.n_fails_by_invalid_partner}"
                     f" Diff:{self.n_fails_by_diff}")
