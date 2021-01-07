from unittest import TestCase
from stackstats import stats
from stackstats.stats import to_timestamp


class RetrieveAPIDataTest(TestCase):

    def test_retrieve_answers(self):
        answers = stats.retrieve_answers(to_timestamp("20200202 10:00:00"), to_timestamp("20200202 10:02:00"))
        self.assertIsInstance(answers, list)

    def test_retrieve_comment_counts(self):
        cntrs = stats.retrieve_comment_counts([65285866, 65285883, 65285957])
        self.assertIsInstance(cntrs, list)
