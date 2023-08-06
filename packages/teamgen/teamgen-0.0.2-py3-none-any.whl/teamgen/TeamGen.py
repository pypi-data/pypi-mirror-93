import logging
from .Meeting import Meeting
from .round import MatchRound
from .meeting_history import MeetingHistory
from .random_builder import RandomMeetingBuilder
from .combo_builder import ComboMeetingBuilder

logger = logging.getLogger(__name__)


class TeamGen(object):
    def __init__(self, courts, num_seq,
                 men, women,
                 low_threshold=0.75):
        self.n_courts = courts
        self.history = MeetingHistory(
            group1=men,
            group2=women,
            low_threshold=low_threshold
        )
        self.builder = RandomMeetingBuilder(
            courts, num_seq, men, women,
            history=self.history
        )
        self.meeting = Meeting(courts, num_seq, men, women,
                               history=self.history,
                               builder=self.builder)
        self.diff_max = 0.1
        self.MaxBadDiff = 1.0
        self.n_sequences = num_seq
        self.iterLimit = 1000

    def generate_rounds(self,
                        b_allow_duplicates: bool = False,
                        iterations: int = None,
                        max_tries: int = 20,
                        special_requests=None):
        self.meeting.restart()

        self.meeting.see_player_once = not b_allow_duplicates
        if iterations is not None:
            self.meeting.max_iterations = iterations

        while self.meeting.round_count < self.n_sequences:

            round = self.generate_round(self.meeting, max_tries=max_tries)

            if round is None:
                self.meeting.print_check_stats()
                logger.info("Failed to build the sequence.")
                return None
            else:
                round.display()

                self.meeting.add_round(round)

                d_max, d_avg, diff_list = round.diff_stats()
                diffs = ",".join(["%5.3f" % x for x in diff_list])
                logger.info("Found a set sequence with DiffMax:%5.3f Max:%3.3f Avg:%5.3f List:%s" % (
                    self.diff_max, d_max, d_avg, diffs))

                status_msg = f"Generated {self.meeting.round_count} sequence(s)"
                logger.info(status_msg)

        return self.meeting.get_rounds()

    @staticmethod
    def generate_round(meeting, max_tries: int = 20):
        """
        Generate a new round in the meeting

        It won't matter how many rounds exists, we can just generate a new round given
        the current meeting statistics.

        ToDo: Isolate the statistics from the meeting, so we can generate them using other methods
        :param meeting:
        :param max_tries:
        :return:
        """
        quality_range = [98, 35, -5]
        diff_range = [0.0, 1.0, 0.1]
        min_quality = quality_range[0]
        max_diff = diff_range[0]
        round = None

        while min_quality >= quality_range[1] and max_diff < diff_range[1] and not round:
            results = meeting.get_new_round(
                diff_max=max_diff,
                quality_min=min_quality,
                max_tries=max_tries)

            round, stats = results
            min_found_diff = stats.min_diff
            min_q = stats.min_q
            max_q = stats.max_q
            status_msg = (f"Quality Stats: min:{min_q} max:{max_q}"
                          f" QThresh:{min_quality} DThresh:{max_diff}")
            logger.info(status_msg)

            if not round:
                # Increase the quality then the diff
                min_quality += quality_range[2]
                max_diff += diff_range[2]
                # if min_quality <= quality_range[1]:
                #     min_quality = quality_range[0]
                #     max_diff += diff_range[2]
                logger.debug(f"Criteria updated. QThres:{min_quality} DThres:{max_diff}")

        return round

    @staticmethod
    def display_sequences(seq):
        for s in seq:
            s.display()

    @staticmethod
    def show_all_diffs(seq):
        [s.show_diffs() for s in seq]
