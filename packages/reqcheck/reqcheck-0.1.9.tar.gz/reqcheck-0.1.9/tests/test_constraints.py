import mock
import unittest

from datetime import timedelta

import reqcheck.constraints as constraints
import reqcheck.exceptions as exceptions


class ConstraintCallTest(unittest.TestCase):
    def setUp(self):
        self.check = constraints.Constraint()
        self.check.check_result = mock.Mock(return_value = False)
        self.check.raise_exception = mock.Mock()
        self.result = {'age': timedelta(days = 3)}

    def testChecksResult(self):
        self.check(self.result)

        self.check.check_result.assert_called_with(self.result)

    def testRaisesExceptionIfCheckResultReturnsTrue(self):
        self.check.check_result.return_value = True

        self.check(self.result)

        self.check.raise_exception.assert_called_with(self.result)

    def testDoesNotRaiseExceptionIfCheckResultReturnsFalse(self):
        self.check.check_result.return_value = False

        self.check(self.result)

        self.assertFalse(self.check.raise_exception.called)


class MaxVersionsBehindInitTest(unittest.TestCase):
    def testSettings(self):
        check = constraints.MaxVersionsBehind(3)
        self.assertEqual(3, check.max_versions_behind)


class MaxVersionsBehindCheckResultTest(unittest.TestCase):
    def setUp(self):
        self.check = constraints.MaxVersionsBehind(3)

    def testWhenResultValueMissing(self):
        self.assertFalse(self.check.check_result({}))

    def testWhenResultValueIsNone(self):
        self.assertFalse(self.check.check_result({'behind_num_versions': None}))

    def testWhenNotBehind(self):
        self.assertFalse(self.check.check_result({'behind_num_versions': 2}))

    def testWhenBehind(self):
        self.assertTrue(self.check.check_result({'behind_num_versions': 4}))


class MaxVersionsBehindRaiseExceptionTest(unittest.TestCase):
    def setUp(self):
        self.check = constraints.MaxVersionsBehind(3)

    def testResult(self):
        with self.assertRaises(exceptions.ConstraintFailure) as context:
            self.check.raise_exception({'pkg_name': 'test_pkg', 'behind_num_versions': 4})
        self.assertEqual('Package test_pkg exceeds max number of versions behind latest version (4 > 3 versions)', str(context.exception))


class MaxDaysBehindInitTest(unittest.TestCase):
    def testSettings(self):
        check = constraints.MaxDaysBehind(3)
        self.assertEqual(3, check.max_days_behind)
        self.assertEqual(timedelta(days = 3), check.max_time_delta)


class MaxDaysBehindCheckResultTest(unittest.TestCase):
    def setUp(self):
        self.check = constraints.MaxDaysBehind(3)

    def testWhenResultValueMissing(self):
        self.assertFalse(self.check.check_result({}))

    def testWhenResultValueIsNone(self):
        self.assertFalse(self.check.check_result({'behind_time_delta': None}))

    def testWhenNotBehind(self):
        self.assertFalse(self.check.check_result({'behind_time_delta': timedelta(days = 2)}))

    def testWhenBehind(self):
        self.assertTrue(self.check.check_result({'behind_time_delta': timedelta(days = 4)}))


class MaxDaysBehindRaiseExceptionTest(unittest.TestCase):
    def setUp(self):
        self.check = constraints.MaxDaysBehind(3)

    def testResult(self):
        with self.assertRaises(exceptions.ConstraintFailure) as context:
            self.check.raise_exception({'pkg_name': 'test_pkg', 'behind_time_delta': timedelta(days = 4)})
        self.assertEqual('Package test_pkg exceeds max number of days behind latest version (4 > 3 days)', str(context.exception))


class MaxAgeInitTest(unittest.TestCase):
    def testSettings(self):
        check = constraints.MaxAge(3)
        self.assertEqual(3, check.max_age)
        self.assertEqual(timedelta(days = 3), check.max_time_delta)


class MaxAgeCheckResultTest(unittest.TestCase):
    def setUp(self):
        self.check = constraints.MaxAge(3)

    def testWhenResultValueMissing(self):
        self.assertFalse(self.check.check_result({}))

    def testWhenResultValueIsNone(self):
        self.assertFalse(self.check.check_result({'age': None}))

    def testWhenNotOlder(self):
        self.assertFalse(self.check.check_result({'age': timedelta(days = 2)}))

    def testWhenOlder(self):
        self.assertTrue(self.check.check_result({'age': timedelta(days = 4)}))


class MaxAgeRaiseExceptionTest(unittest.TestCase):
    def setUp(self):
        self.check = constraints.MaxAge(3)

    def testResult(self):
        with self.assertRaises(exceptions.ConstraintFailure) as context:
            self.check.raise_exception({'pkg_name': 'test_pkg', 'age': timedelta(days = 4)})
        self.assertEqual('Package test_pkg exceeds max age (4 > 3 days)', str(context.exception))


class CheckConstraintsTest(unittest.TestCase):
    def setUp(self):
        self.results = [
            {'pkg_name': 'pkg1', 'behind_num_versions': 3, 'age': timedelta(days = 128)},
            {'pkg_name': 'pkg2', 'behind_num_versions': 5, 'age': timedelta(days = 274)},
            {'pkg_name': 'pkg3', 'behind_num_versions': 1, 'age': timedelta(days = 45)},
        ]
        self.checks = [constraints.MaxVersionsBehind(5), constraints.MaxAge(365)]

    def testChecksResultsOnAllConstraints(self):
        for check in self.checks:
            check.check_result = mock.Mock(return_value = False)

        constraints.check_constraints(self.results, self.checks)

        for check in self.checks:
            check.check_result.assert_has_calls([mock.call(result) for result in self.results])

    def testWhenAllConstraintsPass(self):
        self.assertEqual([], constraints.check_constraints(self.results, self.checks))

    def testWhenConstraintsFail(self):
        self.results[0]['behind_num_versions'] = 7
        self.results[2]['age'] = timedelta(days = 420)

        self.assertEqual([
            'ConstraintFailure: Package pkg1 exceeds max number of versions behind latest version (7 > 5 versions)',
            'ConstraintFailure: Package pkg3 exceeds max age (420 > 365 days)',
        ], constraints.check_constraints(self.results, self.checks))
