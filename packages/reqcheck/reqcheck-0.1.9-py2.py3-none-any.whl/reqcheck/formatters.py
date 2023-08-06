from tabulate import tabulate


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


def format_behind(num_versions, time_delta):
    return '{0} ({1})'.format(num_versions_to_str(num_versions), timedelta_to_str(time_delta))


def format_results(results):
    fields = [
        ('pkg_name', 'Package'),
        ('current_version', 'Current Version'),
        ('latest_version', 'Latest Version'),
        ('behind_str', 'Behind'),
        ('age_str', 'Age'),
    ]
    table = [tuple(r[f[0]] for f in fields) for r in sorted(results, key = lambda r: r['pkg_name'])]
    headers = [f[1] for f in fields]
    return tabulate(table, headers = headers).strip()
