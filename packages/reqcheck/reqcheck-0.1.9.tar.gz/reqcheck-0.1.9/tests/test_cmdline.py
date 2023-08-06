import mock
import six
import sys
import unittest

from datetime import timedelta

import reqcheck
import reqcheck.cmdline as cmdline
import reqcheck.constraints as constraints


class CapturedIO:
    def __init__(self, channel, initial_value = None):
        self.channel = channel
        self.initial_value = initial_value

    def __enter__(self):
        self._backup = getattr(sys, self.channel)
        self.captured = six.StringIO(self.initial_value)
        setattr(sys, self.channel, self.captured)
        return self

    def __exit__(self, *args):
        setattr(sys, self.channel, self._backup)

    def read(self):
        return self.captured.getvalue()

    def write(self, data):
        self.captured.write(data)


class CmdlineTest(unittest.TestCase):
    def setUp(self):
        self.check_pkgs_patcher = mock.patch('reqcheck.packages.check_pkgs')
        self.check_pkgs_mock = self.check_pkgs_patcher.start()

        self.format_results_patcher = mock.patch('reqcheck.formatters.format_results')
        self.format_results_mock = self.format_results_patcher.start()

        self.check_constraints_patcher = mock.patch('reqcheck.constraints.check_constraints')
        self.check_constraints_mock = self.check_constraints_patcher.start()
        self.check_constraints_mock.return_value = []

        self.results = [
            {'pkg_name': 'pkg3', 'age': timedelta(days = 128)},
            {'pkg_name': 'pkg3', 'age': timedelta(days = 286)},
            {'pkg_name': 'pkg3', 'age': timedelta(days = 45)},
        ]
        self.check_pkgs_mock.return_value = self.results

    def tearDown(self):
        self.check_pkgs_patcher.stop()
        self.format_results_patcher.stop()
        self.check_constraints_patcher.stop()

    def testExitsWithErrorCodeAndPrintsToStderrWhenCommandLineError(self):
        with CapturedIO('stderr') as captured:
            self.assertRaises(SystemExit, cmdline.cmdline, ['-bad', 'param'])
            self.assertTrue(len(captured.read()) > 0)

    def testIntegerLessThanZero(self):
        with CapturedIO('stderr') as captured:
            self.assertRaises(SystemExit, cmdline.cmdline, ['--max-age', '-1', 'pkg1==1.0.0'])
            self.assertTrue(len(captured.read()) > 0)

    def testVersion(self):
        with CapturedIO('stdout') as captured:
            cmdline.cmdline(['--version'])
            self.assertEqual('{0}\n'.format(reqcheck.__version__), captured.read())

    def testWithPkgsOnCommandLine(self):
        cmdline.cmdline(['pkg1==1.0.0', 'pkg2==1.0.1'])

        self.check_pkgs_mock.assert_called_with('pkg1==1.0.0\npkg2==1.0.1')

    @mock.patch('reqcheck.packages.get_venv_pkgs')
    def testWithVenv(self, get_venv_pkgs_mock):
        pkgs = 'pkg1==1.0.1\npkg2==2.0.1'
        get_venv_pkgs_mock.return_value = pkgs

        cmdline.cmdline(['-v', '/test/venv'])

        get_venv_pkgs_mock.assert_called_with('/test/venv')
        self.check_pkgs_mock.assert_called_with(pkgs)

    def testWithStdin(self):
        pkgs = 'pkg1==1.1\npkg2==1.2'

        with CapturedIO('stdin', pkgs) as captured:
            cmdline.cmdline([])

        self.check_pkgs_mock.assert_called_with(pkgs)

    def testPrintsResults(self):
        self.format_results_mock.return_value = 'test_results'
        with CapturedIO('stdout') as captured:
            cmdline.cmdline(['pkg1==1.0.0', 'pkg2==1.0.1'])

        self.format_results_mock.assert_called_with(self.results)
        self.assertEqual('test_results\n', captured.read())

    def testWithConstraints(self):
        cmdline.cmdline(['--max-versions-behind', '5', '--max-days-behind', '225', '--max-age', '365', 'pkg1==1.0.0'])

        self.check_constraints_mock.assert_called_with(self.results, mock.ANY)

        checks = self.check_constraints_mock.call_args_list[0][0][1]
        self.assertEqual(3, len(checks))

        self.assertTrue(isinstance(checks[0], constraints.MaxVersionsBehind))
        self.assertEqual(5, checks[0].max_versions_behind)

        self.assertTrue(isinstance(checks[1], constraints.MaxDaysBehind))
        self.assertEqual(225, checks[1].max_days_behind)

        self.assertTrue(isinstance(checks[2], constraints.MaxAge))
        self.assertEqual(365, checks[2].max_age)

    def testWhenConstraintsFail(self):
        self.format_results_mock.return_value = 'test_results'
        self.check_constraints_mock.return_value = ['error1', 'error2']

        with CapturedIO('stdout') as capture_stdout, CapturedIO('stderr') as capture_stderr:
            self.assertRaises(SystemExit, cmdline.cmdline, ['--max-versions-behind', '5', 'pkg1==1.0.0'])
            self.assertEqual('test_results\n', capture_stdout.read())
            self.assertEqual('error1\nerror2\n', capture_stderr.read())
