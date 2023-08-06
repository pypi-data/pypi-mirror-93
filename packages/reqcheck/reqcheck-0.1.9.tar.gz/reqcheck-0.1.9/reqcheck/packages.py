import os
import requests
import six
import subprocess
import sys

from datetime import datetime
from pkg_resources import parse_version
from requests.exceptions import RequestException

import reqcheck
import reqcheck.defines as defines
import reqcheck.exceptions as exceptions
import reqcheck.versions as versions


def get_pkg_info(pkg_name):
    url = defines.PYPI_PKG_JSON_URL.format(pkg_name = pkg_name)

    try:
        response = requests.get(url)
    except RequestException as e:
        reqcheck.logger.warn(str(e))
        return None

    try:
        return response.json()
    except (TypeError, ValueError) as e:
        reqcheck.logger.warn(str(e))
        return None


def get_pkg_versions(pkg_name):
    info = get_pkg_info(pkg_name)
    if info is None:
        return []

    all_versions = []
    releases = info.get('releases', {})
    for version, uploads in six.iteritems(releases):
        if len(uploads) == 0:
            continue
        upload_times = [datetime.strptime(u['upload_time'], '%Y-%m-%dT%H:%M:%S') for u in uploads]
        all_versions.append({
            'version': parse_version(version),
            'last_upload': sorted(upload_times)[-1],
        })

    return list(sorted(all_versions, key = lambda v: v['version']))


def get_venv_pip(venv):
    for path in [
        os.path.join(venv, 'bin', 'pip'),
        os.path.join(venv, 'Scripts', 'pip.exe'),
    ]:
        if os.path.exists(path):
            return path
    raise exceptions.PipMissing()


def get_venv_pkgs(venv):
    pip = get_venv_pip(venv)
    process = subprocess.Popen([pip, '-q', 'freeze'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode != 0:
        raise exceptions.PipFailed()
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


def check_pkgs(pkgs_str):
    results = []

    today = datetime.now()
    for pkg_name, current_version in parse_pkgs(pkgs_str):
        all_versions = get_pkg_versions(pkg_name)
        latest_version = all_versions[-1]['version'] if len(all_versions) > 0 else 'unknown'

        behind_nv, behind_td, behind_str = versions.determine_behind(all_versions, current_version, latest_version)
        age, age_str = versions.determine_age(all_versions, current_version, today)

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
