import mock
import unittest

from datetime import timedelta
from pkg_resources import parse_version

import reqcheck.formatters as formatters


class NumVersionsToStrTest(unittest.TestCase):
    def testWithNone(self):
        self.assertEqual('unknown', formatters.num_versions_to_str(None))

    def testWithLessThanZero(self):
        self.assertEqual('unknown', formatters.num_versions_to_str(-1))

    def testWithZero(self):
        self.assertEqual('same version', formatters.num_versions_to_str(0))

    def testWithOne(self):
        self.assertEqual('-1 version', formatters.num_versions_to_str(1))

    def testWithMoreThanOne(self):
        self.assertEqual('-2 versions', formatters.num_versions_to_str(2))


class TimeDeltaToStrTest(unittest.TestCase):
    def testWithNone(self):
        self.assertEqual('unknown', formatters.timedelta_to_str(None))

    def testWhenLessThanOneDay(self):
        self.assertEqual('< 1 day', formatters.timedelta_to_str(timedelta(minutes = 30)))

    def testResultWithAllUnits(self):
        self.assertEqual('~ 2 years 3 days', formatters.timedelta_to_str(timedelta(days = 733, minutes = 2)))

    def testSingularEndings(self):
        self.assertEqual('~ 1 day', formatters.timedelta_to_str(timedelta(days = 1)))
        self.assertEqual('~ 1 year', formatters.timedelta_to_str(timedelta(days = 365)))


class FormatBehindTest(unittest.TestCase):
    def testResult(self):
        result = formatters.format_behind(5, timedelta(days = 523, seconds = 5234))
        self.assertEqual('-5 versions (~ 1 year 158 days)', result)


class FormatResultsTest(unittest.TestCase):
    def setUp(self):
        self.tabulate_patcher = mock.patch('reqcheck.formatters.tabulate')
        self.tabulate_mock = self.tabulate_patcher.start()
        self.tabulate_mock.return_value = 'test_output'
        self.results = [
            {
                'pkg_name': 'pkg2',
                'current_version': parse_version('2.0.0'),
                'latest_version': parse_version('2.0.2'),
                'behind_str': '-2 versions (~ 2 years 1 day)',
                'age_str': '~ 2 years 12 days (2018-12-05)',
            }, {
                'pkg_name': 'pkg1',
                'current_version': parse_version('1.0.0'),
                'latest_version': parse_version('1.0.2'),
                'behind_str': '-2 versions (< 1 day)',
                'age_str': '< 1 day (2020-12-17)',
            }, {
                'pkg_name': 'pkg3',
                'current_version': parse_version('3.0.0'),
                'latest_version': parse_version('3.0.2'),
                'behind_str': '-2 versions (~ 3 years 2 days)',
                'age_str': '~ 4 years 10 days (2016-12-07)',
            },
        ]

    def tearDown(self):
        self.tabulate_patcher.stop()

    def testCallsTabulateToProduceOutput(self):
        formatters.format_results(self.results)

        # Table is sorted by pkg_name
        expected_table = [
            ('pkg1', parse_version('1.0.0'), parse_version('1.0.2'), '-2 versions (< 1 day)', '< 1 day (2020-12-17)'),
            ('pkg2', parse_version('2.0.0'), parse_version('2.0.2'), '-2 versions (~ 2 years 1 day)', '~ 2 years 12 days (2018-12-05)'),
            ('pkg3', parse_version('3.0.0'), parse_version('3.0.2'), '-2 versions (~ 3 years 2 days)', '~ 4 years 10 days (2016-12-07)'),
        ]
        expected_headers = ['Package', 'Current Version', 'Latest Version', 'Behind', 'Age']
        self.tabulate_mock.assert_called_with(expected_table, headers = expected_headers)

    def testResult(self):
        result = formatters.format_results(self.results)

        self.assertEqual('test_output', result)

    def testStripsTabulateOutput(self):
        self.tabulate_mock.return_value = 'test_output\n\n'

        result = formatters.format_results(self.results)

        self.assertEqual('test_output', result)
