import mock
import os
import shutil
import subprocess
import tempfile
import unittest

from contextlib import contextmanager
from datetime import datetime, timedelta
from pkg_resources import parse_version
from requests.exceptions import RequestException

import reqcheck.exceptions as exceptions
import reqcheck.packages as packages


@contextmanager
def mocked_now(now):
    class MockDateTime(datetime):
        @classmethod
        def now(self):
            return now

    try:
        original_datetime = packages.datetime
        packages.datetime = MockDateTime
        yield
    finally:
        packages.datetime = original_datetime


class GetPkgInfoTest(unittest.TestCase):
    def setUp(self):
        self.get_patcher = mock.patch('requests.get')
        self.get_mock = self.get_patcher.start()

        self.response_mock = mock.Mock()
        self.get_mock.return_value = self.response_mock

    def tearDown(self):
        self.get_patcher.stop()

    def testMakesRequestToPypi(self):
        packages.get_pkg_info('test_pkg')

        self.get_mock.assert_called_with('https://pypi.python.org/pypi/test_pkg/json')

    def testReturnsNoneWhenRequestRaisesException(self):
        self.get_mock.side_effect = RequestException()

        self.assertIsNone(packages.get_pkg_info('test_pkg'))

    def testReturnsNoneWhenResponseContentIsNone(self):
        self.response_mock.json.return_value = None

        self.assertIsNone(packages.get_pkg_info('test_pkg'))

    def testReturnsNoneWhenFailedToParseContent(self):
        self.response_mock.json.side_effect = ValueError()

        self.assertIsNone(packages.get_pkg_info('test_pkg'))

    def testResultWithSuccess(self):
        self.response_mock.json.return_value = {'a':1}

        self.assertDictEqual({'a':1}, packages.get_pkg_info('test_pkg'))


class GetPkgVersionsTest(unittest.TestCase):
    def setUp(self):
        self.get_pkg_info_patcher = mock.patch('reqcheck.packages.get_pkg_info')
        self.get_pkg_info_mock = self.get_pkg_info_patcher.start()

    def testGetsPackageInfo(self):
        packages.get_pkg_versions('test_pkg')

        self.get_pkg_info_mock.assert_called_with('test_pkg')

    def testReturnsEmptyListWhenFailedToGetPackageInfo(self):
        self.get_pkg_info_mock.return_value = None

        self.assertEqual([], packages.get_pkg_versions('test_pkg'))

    def testReturnsEmptyListWhenReleasesNotSpecified(self):
        self.get_pkg_info_mock.return_value = {}

        self.assertEqual([], packages.get_pkg_versions('test_pkg'))

    def testReturnsEmptyListWhenNoReleases(self):
        self.get_pkg_info_mock.return_value = {'releases': {}}

        self.assertEqual([], packages.get_pkg_versions('test_pkg'))

    def testParsesAndSelectsLatestUploadTime(self):
        self.get_pkg_info_mock.return_value = {
            'releases': {
                '0.9': [{'upload_time': '2016-10-22T07:15:20'}],
                '1.0': [{'upload_time': '2016-10-22T12:07:15'}, {'upload_time': '2016-10-22T13:11:15'}],
                '1.1': [{'upload_time': '2016-10-23T14:51:50'}, {'upload_time': '2016-10-23T12:14:50'}],
            },
        }
        expected = [
            {'version': parse_version('0.9'), 'last_upload': datetime(2016, 10, 22, 7, 15, 20)},
            {'version': parse_version('1.0'), 'last_upload': datetime(2016, 10, 22, 13, 11, 15)},
            {'version': parse_version('1.1'), 'last_upload': datetime(2016, 10, 23, 14, 51, 50)},
        ]
        self.assertEqual(expected, packages.get_pkg_versions('test_pkg'))

    def testIgnoreVersionsWithoutUploads(self):
        self.get_pkg_info_mock.return_value = {
            'releases': {
                '0.9': [{'upload_time': '2016-10-22T07:15:20'}],
                '1.0': [],
                '1.1': [{'upload_time': '2016-10-23T14:51:50'}],
            },
        }

        result = packages.get_pkg_versions('test_pkg')

        expected = [parse_version(v) for v in ('0.9', '1.1')]
        self.assertEqual(expected, [row['version'] for row in result])

    def testSortedByVersion(self):
        self.get_pkg_info_mock.return_value = {
            'releases': {
                '0.9.1': [{'upload_time': '2016-10-22T07:15:20'}],
                '0.8.0': [{'upload_time': '2016-10-22T12:07:15'}],
                '0.9.0.rc1': [{'upload_time': '2016-10-23T14:51:50'}],
            },
        }

        result = packages.get_pkg_versions('test_pkg')

        expected = [parse_version(v) for v in ('0.8.0', '0.9.0.rc1', '0.9.1')]
        self.assertEqual(expected, [row['version'] for row in result])


class GetVenvPipTest(unittest.TestCase):
    def setUp(self):
        self.venv_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.venv_dir)

    def tempFile(self, *path):
        os.makedirs(os.path.join(self.venv_dir, *path[:-1]))
        with open(os.path.join(self.venv_dir, *path), 'w') as file:
            file.write('test_file')

    def testWithBinPip(self):
        self.tempFile('bin', 'pip')

        expected = os.path.join(self.venv_dir, 'bin', 'pip')
        self.assertEqual(expected, packages.get_venv_pip(self.venv_dir))

    def testWithScriptsPipEXE(self):
        self.tempFile('Scripts', 'pip.exe')

        expected = os.path.join(self.venv_dir, 'Scripts', 'pip.exe')
        self.assertEqual(expected, packages.get_venv_pip(self.venv_dir))

    def testWhenPipMissing(self):
        self.assertRaises(exceptions.PipMissing, packages.get_venv_pip, self.venv_dir)


class GetVenvPkgsTest(unittest.TestCase):
    def setUp(self):
        self.get_venv_pip_patcher = mock.patch('reqcheck.packages.get_venv_pip')
        self.get_venv_pip_mock = self.get_venv_pip_patcher.start()

        self.popen_patcher = mock.patch('subprocess.Popen')
        self.popen_mock = self.popen_patcher.start()

        self.process_mock = mock.Mock()
        self.process_mock.returncode = 0
        self.process_mock.communicate.return_value = (None, None)
        self.popen_mock.return_value = self.process_mock

    def tearDown(self):
        self.get_venv_pip_patcher.stop()
        self.popen_patcher.stop()

    def testGetsVenvPip(self):
        packages.get_venv_pkgs('/test/venv')

        self.get_venv_pip_mock.assert_called_with('/test/venv')

    def testStartsProcess(self):
        self.get_venv_pip_mock.return_value = '/test/venv/bin/pip'

        packages.get_venv_pkgs('/test/venv')

        self.popen_mock.assert_called_with(
            ['/test/venv/bin/pip', '-q', 'freeze'],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )

    def testCommunicatesWithProcess(self):
        packages.get_venv_pkgs('/test/venv')

        self.process_mock.communicate.assert_called_with()

    def testRaisesExceptionWhenNonZeroReturnCode(self):
        self.process_mock.returncode = 1

        self.assertRaises(exceptions.PipFailed, packages.get_venv_pkgs, '/test/venv')

    def testReturnsOutput(self):
        self.process_mock.communicate.return_value = ('test_output', None)

        self.assertEqual('test_output', packages.get_venv_pkgs('/test/venv'))

    def testConvertsBytesToStr(self):
        self.process_mock.communicate.return_value = (b'test_output', None)

        self.assertEqual('test_output', packages.get_venv_pkgs('/test/venv'))


class GetStdinPkgsTest(unittest.TestCase):
    def setUp(self):
        self.stdin_patcher = mock.patch('sys.stdin')
        self.stdin_mock = self.stdin_patcher.start()

    def tearDown(self):
        self.stdin_patcher.stop()

    def testReadsAndReturnsStdin(self):
        self.stdin_mock.read.return_value = 'test_stdin'

        self.assertEqual('test_stdin', packages.get_stdin_pkgs())
        self.stdin_mock.read.assert_called_with()


class ParsePkgsTest(unittest.TestCase):
    def testReturnsEmptyListWhenNoPackages(self):
        self.assertEqual([], packages.parse_pkgs(None))
        self.assertEqual([], packages.parse_pkgs(''))
        self.assertEqual([], packages.parse_pkgs(' \n\t\n'))

    def testParsesBasicPackageVersion(self):
        self.assertEqual([('test_pkg', parse_version('1.0.1'))], packages.parse_pkgs('test_pkg==1.0.1'))

    def testSkipsBlankLines(self):
        pkgs = '''
pkg1==1.0.1

pkg2==1.0.2

'''
        expected = [('pkg1', parse_version('1.0.1')), ('pkg2', parse_version('1.0.2'))]
        self.assertEqual(expected, packages.parse_pkgs(pkgs))

    def testReturnsPackageWithNoneVersionWhenVersionMissing(self):
        self.assertEqual([('test_pkg', None)], packages.parse_pkgs('test_pkg'))


class CheckPkgsTest(unittest.TestCase):
    def setUp(self):
        self.get_pkg_versions_patcher = mock.patch('reqcheck.packages.get_pkg_versions')
        self.get_pkg_versions_mock = self.get_pkg_versions_patcher.start()
        self.get_pkg_versions_mock.return_value = []

    def tearDown(self):
        self.get_pkg_versions_patcher.stop()

    def testWithEmptyPkgs(self):
        self.assertEqual([], packages.check_pkgs(None))
        self.assertEqual([], packages.check_pkgs(''))
        self.assertEqual([], packages.check_pkgs(' \n \t  '))

    def testGetsPackageVersions(self):
        packages.check_pkgs('pkg1==1.0.1\npkg2==1.0.2')

        self.get_pkg_versions_mock.assert_has_calls([mock.call('pkg1'), mock.call('pkg2')])

    def testResults(self):
        self.maxDiff = None

        self.get_pkg_versions_mock.side_effect = iter([
            [
                {'version': parse_version('1.0.0'), 'last_upload': datetime(2014, 10, 21, 17, 14, 45)},
                {'version': parse_version('1.0.1'), 'last_upload': datetime(2016, 10, 22, 14, 14, 45)},
                {'version': parse_version('1.0.2'), 'last_upload': datetime(2016, 10, 22, 16, 14, 45)},
            ], [

                {'version': parse_version('2.0.0'), 'last_upload': datetime(2014, 10, 19, 11, 14, 45)},
                {'version': parse_version('2.0.1'), 'last_upload': datetime(2016, 10, 20, 14, 14, 45)},
                {'version': parse_version('2.0.2'), 'last_upload': datetime(2016, 10, 20, 16, 14, 45)},
            ], [

                {'version': parse_version('3.0.0'), 'last_upload': datetime(2014, 10, 19, 11, 14, 45)},
                {'version': parse_version('3.0.1'), 'last_upload': datetime(2016, 10, 20, 14, 14, 45)},
                {'version': parse_version('3.0.2'), 'last_upload': datetime(2016, 10, 20, 16, 14, 45)},
            ]
        ])

        with mocked_now(datetime(2021, 1, 28, 18, 30, 45)):
            result = packages.check_pkgs('pkg1==1.0.0\npkg2==2.0.1\npkg3==3.0.2')

        self.assertEqual([
            {
                'pkg_name': 'pkg1',
                'current_version': parse_version('1.0.0'),
                'latest_version': parse_version('1.0.2'),
                'behind_num_versions': 2,
                'behind_time_delta': timedelta(days = 731, hours = 23),
                'behind_str': '-2 versions (~ 2 years 1 day)',
                'age': timedelta(days = 2291, seconds = 4560),
                'age_str': '~ 6 years 101 days (2014-10-21)',
            }, {
                'pkg_name': 'pkg2',
                'current_version': parse_version('2.0.1'),
                'latest_version': parse_version('2.0.2'),
                'behind_num_versions': 1,
                'behind_time_delta': timedelta(hours = 2),
                'behind_str': '-1 version (< 1 day)',
                'age': timedelta(days = 1561, seconds = 15360),
                'age_str': '~ 4 years 101 days (2016-10-20)',
            }, {
                'pkg_name': 'pkg3',
                'current_version': parse_version('3.0.2'),
                'latest_version': parse_version('3.0.2'),
                'behind_num_versions': 0,
                'behind_time_delta': timedelta(0),
                'behind_str': 'latest',
                'age': timedelta(days = 1561, seconds = 8160),
                'age_str': '~ 4 years 101 days (2016-10-20)',
            },
        ], result)
