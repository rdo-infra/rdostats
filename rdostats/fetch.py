import bugzilla
import arrow

import defaults

fields = [
    'assigned_to',
    'component',
    'creation_time',
    'creator',
    'creator',
    'depends_on',
    'fixed_in',
    'id',
    'keywords',
    'last_change_time',
    'status',
    'summary',
    'target_milestone',
    'target_release',
    'url',
    'version',
    'weburl',
]


def fetch_bugs(url=defaults.url,
               product=defaults.product,
               status=defaults.status_all):
    bz = bugzilla.Bugzilla(url)
    bugs = bz.query(bz.build_query(
        product=product,
        status=status))

    bugs = [dict(((k, getattr(bug, k)) for k in fields)) for bug in bugs]
    metadata = {
        'url': url,
        'product': product,
        'status': status,
        'date': arrow.now(),
    }

    return {
        'bugs': bugs,
        'metadata': metadata,
    }
