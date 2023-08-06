import unittest

from datetime import datetime, timedelta
from pkg_resources import parse_version

import reqcheck.versions as versions


class GetBehindNumVersionsTest(unittest.TestCase):
    def setUp(self):
        self.versions = [
            {'version': parse_version('1.0.1')},
            {'version': parse_version('1.0.2')},
            {'version': parse_version('1.0.3')},
        ]

    def testWhenVersionNotFound(self):
        self.assertEqual(None, versions.get_behind_num_versions(self.versions, parse_version('1.0.1'), parse_version('5.1')))
        self.assertEqual(None, versions.get_behind_num_versions(self.versions, parse_version('5.1'), parse_version('1.0.1')))

class GetBehindTimeDeltaTest(unittest.TestCase):
    def setUp(self):
        self.versions = [
            {'version': parse_version('1.0.1'), 'last_upload': datetime(2016, 10, 22, 12, 34, 56)},
            {'version': parse_version('1.0.2'), 'last_upload': datetime(2016, 10, 22, 14, 46, 24)},
        ]

    def testWhenMissingVersion(self):
        self.assertEqual(None, versions.get_behind_time_delta(self.versions, parse_version('1.0.1'), None))
        self.assertEqual(None, versions.get_behind_time_delta(self.versions, None, parse_version('1.0.2')))

    def testWhenVersionsMatch(self):
        version = parse_version('1.0.1')
        self.assertEqual(timedelta(0), versions.get_behind_time_delta(self.versions, version, version))

    def testResult(self):
        expected = self.versions[1]['last_upload'] - self.versions[0]['last_upload']
        self.assertEqual(expected, versions.get_behind_time_delta(self.versions, parse_version('1.0.1'), parse_version('1.0.2')))


class DetermineBehindTest(unittest.TestCase):
    def setUp(self):
        self.versions = [
            {'version': parse_version('1.0.0'), 'last_upload': datetime(2014, 10, 21, 17, 14, 45)},
            {'version': parse_version('1.0.1'), 'last_upload': datetime(2016, 10, 22, 14, 14, 45)},
            {'version': parse_version('1.0.2'), 'last_upload': datetime(2016, 10, 22, 16, 14, 45)},
            {'version': parse_version('1.0.3'), 'last_upload': datetime(2018, 11, 12, 18, 10, 15)},
            {'version': parse_version('1.0.4'), 'last_upload': datetime(2021, 1, 28, 18, 15, 30)},
        ]

    def testWhenBehind(self):
        result = versions.determine_behind(self.versions, parse_version('1.0.1'), parse_version('1.0.4'))
        self.assertEqual((3, timedelta(days = 1559, seconds = 14445), '-3 versions (~ 4 years 99 days)'), result)

    def testWhenLatest(self):
        result = versions.determine_behind(self.versions, parse_version('1.0.4'), parse_version('1.0.4'))
        self.assertEqual((0, timedelta(days = 0), 'latest'), result)


class DetermineAgeTest(unittest.TestCase):
    def setUp(self):
        self.versions = [
            {'version': parse_version('1.0.0'), 'last_upload': datetime(2014, 10, 21, 17, 14, 45)},
            {'version': parse_version('1.0.1'), 'last_upload': datetime(2016, 10, 22, 14, 14, 45)},
            {'version': parse_version('1.0.2'), 'last_upload': datetime(2016, 10, 22, 16, 14, 45)},
            {'version': parse_version('1.0.3'), 'last_upload': datetime(2018, 11, 12, 18, 10, 15)},
            {'version': parse_version('1.0.4'), 'last_upload': datetime(2021, 1, 28, 18, 15, 30)},
        ]

    def testWhenVersionFound(self):
        result = versions.determine_age(self.versions, parse_version('1.0.3'), datetime(2021, 1, 29))
        self.assertEqual((timedelta(days = 808, seconds = 20985), '~ 2 years 78 days (2018-11-12)'), result)

    def testWhenVersionNotFound(self):
        result = versions.determine_age(self.versions, parse_version('1.20.12'), datetime(2021, 1, 29))
        self.assertEqual((None, 'unknown'), result)
