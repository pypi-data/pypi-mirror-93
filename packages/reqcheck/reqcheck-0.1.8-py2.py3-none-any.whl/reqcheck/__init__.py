from __future__ import print_function

import argparse
import logging
import os
import requests
import six
import subprocess
import sys
import tabulate

from datetime import datetime
from pkg_resources import get_distribution, parse_version
from requests.exceptions import RequestException

__version__ = get_distribution('reqcheck').version

PYPI_PKG_JSON_URL = 'https://pypi.python.org/pypi/{pkg_name}/json'

logger = logging.getLogger('reqcheck')

class ReqCheckException(Exception): pass
class PipMissing(ReqCheckException): pass
class PipFailed(ReqCheckException): pass

def get_pkg_info(pkg_name):
    url = PYPI_PKG_JSON_URL.format(pkg_name = pkg_name)

    try:
        response = requests.get(url)
    except RequestException as e:
        logger.warn(str(e))
        return None

    try:
        return response.json()
    except (TypeError, ValueError) as e:
        logger.warn(str(e))
        return None

def get_pkg_versions(pkg_name):
    info = get_pkg_info(pkg_name)
    if info is None:
        return []

    versions = []
    releases = info.get('releases', {})
    for version, uploads in six.iteritems(releases):
        if len(uploads) == 0:
            continue
        upload_times = [datetime.strptime(u['upload_time'], '%Y-%m-%dT%H:%M:%S') for u in uploads]
        versions.append({
            'version': parse_version(version),
            'last_upload': sorted(upload_times)[-1],
        })

    return list(sorted(versions, key = lambda v: v['version']))

def get_venv_pip(venv):
    for path in [
        os.path.join(venv, 'bin', 'pip'),
        os.path.join(venv, 'Scripts', 'pip.exe'),
    ]:
        if os.path.exists(path):
            return path
    raise PipMissing()

def get_venv_pkgs(venv):
    pip = get_venv_pip(venv)
    process = subprocess.Popen([pip, '-q', 'freeze'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        raise PipFailed()
    return out.decode('utf-8') if isinstance(out, bytes) else out

def get_stdin_pkgs():
    return sys.stdin.read()

def parse_pkgs(pkgs_str):
    if pkgs_str is None or pkgs_str.strip() == '':
        return []

    pkgs = []
    for line in pkgs_str.split('\n'):
        pieces = line.strip().split('==')
        if len(pieces) == 1:
            if not pieces[0]:
                continue
            pkgs.append((pieces[0], None))
        else:
            pkgs.append((pieces[0], parse_version(pieces[1])))
    return pkgs

def get_behind_num_versions(versions, version1, version2):
    idx1 = next((i for i, v in enumerate(versions) if v['version'] == version1), None)
    idx2 = next((i for i, v in enumerate(versions) if v['version'] == version2), None)
    return idx2 - idx1 if idx1 is not None and idx2 is not None else None

def get_behind_time_delta(versions, version1, version2):
    version_map = dict((v['version'], v) for v in versions)
    v1 = version_map.get(version1)
    v2 = version_map.get(version2)
    return v2['last_upload'] - v1['last_upload'] if v1 and v2 else None

def determine_behind(versions, current_version, latest_version):
    behind_nv = get_behind_num_versions(versions, current_version, latest_version)
    behind_td = get_behind_time_delta(versions, current_version, latest_version)
    behind_str = 'latest' if current_version == latest_version else format_behind(behind_nv, behind_td)
    return behind_nv, behind_td, behind_str

def format_behind(num_versions, time_delta):
    return '{0} ({1})'.format(num_versions_to_str(num_versions), timedelta_to_str(time_delta))

def determine_age(versions, current_version, from_date):
    version = next((v for v in versions if v['version'] == current_version), None)
    age = from_date - version['last_upload'] if version is not None else None
    if age is None:
        return None, 'unknown'
    return age, '{0} ({1})'.format(timedelta_to_str(age), version['last_upload'].strftime('%Y-%m-%d'))

def num_versions_to_str(nv):
    if nv is None or nv < 0:
        return 'unknown'

    if nv == 0:
        return 'same version'

    lbl = 'versions' if nv > 1 else 'version'
    return '-{0} {1}'.format(nv, lbl)

def timedelta_to_str(td):
    if td is None:
        return 'unknown'

    seconds = int(td.total_seconds())

    unit_pieces = {}
    for unit, unit_secs in [
        ('years', 31536000),
        ('days', 86400),
    ]:
        unit_pieces[unit], seconds = divmod(seconds, unit_secs)

    str_pieces = []
    for unit, endings in [
        ('years', ['year', 'years']),
        ('days', ['day', 'days']),
    ]:
        if unit_pieces[unit] > 0:
            lbl = endings[1] if unit_pieces[unit] > 1 else endings[0]
            str_pieces.append('{0} {1}'.format(unit_pieces[unit], lbl))

    return '~ {0}'.format(' '.join(str_pieces)) if len(str_pieces) > 0 else '< 1 day'

def check_pkgs(pkgs_str):
    results = []

    today = datetime.now()
    for pkg_name, current_version in parse_pkgs(pkgs_str):
        versions = get_pkg_versions(pkg_name)
        latest_version = versions[-1]['version'] if len(versions) > 0 else 'unknown'

        behind_nv, behind_td, behind_str = determine_behind(versions, current_version, latest_version)
        age, age_str = determine_age(versions, current_version, today)

        results.append({
            'pkg_name': pkg_name,
            'current_version': current_version,
            'latest_version': latest_version,
            'behind_num_versions': behind_nv,
            'behind_time_delta': behind_td,
            'behind_str': behind_str,
            'age': age,
            'age_str': age_str,
        })

    return results

def print_results(results):
    fields = [
        ('pkg_name', 'Package'),
        ('current_version', 'Current Version'),
        ('latest_version', 'Latest Version'),
        ('behind_str', 'Behind'),
        ('age_str', 'Age'),
    ]
    table = [tuple(r[f[0]] for f in fields) for r in sorted(results, key = lambda r: r['pkg_name'])]
    headers = [f[1] for f in fields]
    print(tabulate.tabulate(table, headers = headers).strip())

def cmdline(arg_list = None):
    parser = argparse.ArgumentParser('Compare versions of installed packages to latest versions')
    parser.add_argument('--version', action = 'store_true', help = 'Output reqcheck version')
    parser.add_argument('-v', '--venv', help = 'Path to a virtualenv to check')
    parser.add_argument('pkg', nargs = '*', help = 'Package requirement (eg. reqcheck=={0})'.format(__version__))
    args = parser.parse_args(arg_list)

    if args.version:
        print(__version__)
        return

    if args.venv:
        pkgs_str = get_venv_pkgs(args.venv)
    elif args.pkg:
        pkgs_str = '\n'.join(args.pkg)
    else:
        pkgs_str = get_stdin_pkgs()

    results = check_pkgs(pkgs_str)
    print_results(results)
