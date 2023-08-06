from __future__ import print_function

import argparse
import sys

import reqcheck
import reqcheck.constraints as constraints
import reqcheck.formatters as formatters
import reqcheck.packages as packages


def cmdline(arg_list = None):
    parser = argparse.ArgumentParser('Compare versions of installed packages to latest versions')
    parser.add_argument('--version', action = 'store_true', help = 'Output reqcheck version')
    parser.add_argument('-v', '--venv', help = 'Path to a virtualenv to check')
    parser.add_argument('--max-versions-behind', type = int_greater_than_zero, help = 'The maximum number of versions allowed behind latest of any installed package')
    parser.add_argument('--max-days-behind', type = int_greater_than_zero, help = 'The maximum number of days allowed behind latest of any installed package version')
    parser.add_argument('--max-age', type = int_greater_than_zero, help = 'The maximum age (in days) allowed of the installed version of any package')
    parser.add_argument('pkg', nargs = '*', help = 'Package requirement (eg. reqcheck=={0})'.format(reqcheck.__version__))
    args = parser.parse_args(arg_list)

    if args.version:
        print(reqcheck.__version__)
        return

    if args.venv:
        pkgs_str = packages.get_venv_pkgs(args.venv)
    elif args.pkg:
        pkgs_str = '\n'.join(args.pkg)
    else:
        pkgs_str = packages.get_stdin_pkgs()

    results = packages.check_pkgs(pkgs_str)
    print(formatters.format_results(results))

    checks = build_constraints_from_args(args)
    errors = constraints.check_constraints(results, checks)
    if errors:
        print('\n'.join(errors), file = sys.stderr)
        sys.exit(1)


def int_greater_than_zero(val):
    i = int(val)
    if i <= 0:
        raise argparse.ArgumentTypeError('Must be greater than zero')
    return i


def build_constraints_from_args(args):
    checks = []
    if args.max_versions_behind is not None:
        checks.append(constraints.MaxVersionsBehind(args.max_versions_behind))
    if args.max_days_behind is not None:
        checks.append(constraints.MaxDaysBehind(args.max_days_behind))
    if args.max_age is not None:
        checks.append(constraints.MaxAge(args.max_age))
    return checks
