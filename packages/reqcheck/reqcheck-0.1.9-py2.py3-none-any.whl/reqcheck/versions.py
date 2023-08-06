import reqcheck.formatters as formatters


def get_behind_num_versions(all_versions, version1, version2):
    idx1 = next((i for i, v in enumerate(all_versions) if v['version'] == version1), None)
    idx2 = next((i for i, v in enumerate(all_versions) if v['version'] == version2), None)
    return idx2 - idx1 if idx1 is not None and idx2 is not None else None


def get_behind_time_delta(all_versions, version1, version2):
    version_map = dict((v['version'], v) for v in all_versions)
    v1 = version_map.get(version1)
    v2 = version_map.get(version2)
    return v2['last_upload'] - v1['last_upload'] if v1 and v2 else None


def determine_behind(all_versions, current_version, latest_version):
    behind_nv = get_behind_num_versions(all_versions, current_version, latest_version)
    behind_td = get_behind_time_delta(all_versions, current_version, latest_version)
    behind_str = 'latest' if current_version == latest_version else formatters.format_behind(behind_nv, behind_td)
    return behind_nv, behind_td, behind_str


def determine_age(all_versions, current_version, from_date):
    version = next((v for v in all_versions if v['version'] == current_version), None)
    age = from_date - version['last_upload'] if version is not None else None
    if age is None:
        return None, 'unknown'
    return age, '{0} ({1})'.format(formatters.timedelta_to_str(age), version['last_upload'].strftime('%Y-%m-%d'))
