from datetime import timedelta

import reqcheck.exceptions as exceptions


class Constraint:
    def __call__(self, result):
        if self.check_result(result):
            self.raise_exception(result)


class MaxVersionsBehind(Constraint):
    def __init__(self, max_versions_behind):
        self.max_versions_behind = max_versions_behind

    def check_result(self, result):
        behind = result.get('behind_num_versions')
        return behind is not None and behind > self.max_versions_behind

    def raise_exception(self, result):
        tmpl = 'Package {0} exceeds max number of versions behind latest version ({1} > {2} versions)'
        raise exceptions.ConstraintFailure(tmpl.format(result['pkg_name'], result['behind_num_versions'], self.max_versions_behind))


class MaxDaysBehind(Constraint):
    def __init__(self, max_days_behind):
        self.max_days_behind = max_days_behind
        self.max_time_delta = timedelta(days = self.max_days_behind)

    def check_result(self, result):
        behind = result.get('behind_time_delta')
        return behind is not None and behind > self.max_time_delta

    def raise_exception(self, result):
        tmpl = 'Package {0} exceeds max number of days behind latest version ({1} > {2} days)'
        raise exceptions.ConstraintFailure(tmpl.format(result['pkg_name'], result['behind_time_delta'].days, self.max_days_behind))


class MaxAge(Constraint):
    def __init__(self, max_age):
        self.max_age = max_age
        self.max_time_delta = timedelta(days = self.max_age)

    def check_result(self, result):
        age = result.get('age')
        return age is not None and age > self.max_time_delta

    def raise_exception(self, result):
        tmpl = 'Package {0} exceeds max age ({1} > {2} days)'
        raise exceptions.ConstraintFailure(tmpl.format(result['pkg_name'], result['age'].days, self.max_age))


def check_constraints(results, checks):
    errors = []
    for result in results:
        for check in checks:
            try:
                check(result)
            except Exception as exc:
                errors.append('{0}: {1}'.format(type(exc).__name__, str(exc)))
    return errors
