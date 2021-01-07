from unittest import TestCase
from stackstats import stats
from stackstats.stats import to_timestamp


class InputArgumentsTest(TestCase):

    def setUp(self):
        self.parser = stats.create_parser()

    def test_since_date_input(self):
        parsed = self.parser.parse_args(["--since", "20200202", "--until", "20200203"])
        self.assertEqual(parsed.since, "20200202")

    def test_until_date_input(self):
        parsed = self.parser.parse_args(["--since", "20200202", "--until", "20200203"])
        self.assertEqual(parsed.until, "20200203")

    def test_output_format_input(self):
        parsed = self.parser.parse_args(["--since", "20200202", "--until", "20200203", "--output-format", "csv"])
        self.assertEqual(parsed.output_format, "csv")
