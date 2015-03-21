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
    'resolution',
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


def update_bugs(data, url=defaults.url):
    bz = bugzilla.Bugzilla(url)
    update = bz.getbugs([bug['id'] for bug in data['bugs']])
    update = dict((bug.id, bug) for bug in update)

    for bug in data['bugs']:
        new_bug = update[bug['id']]
        bug['new_status'] = new_bug.status
        bug['resolution'] = new_bug.resolution
        bug['last_change_time'] = (
            arrow.get(new_bug.last_change_time.timetuple()))

        if bug['status'] != new_bug.status:
            bug['history'] = (
                new_bug.get_history()['bugs'][0]['history'])

    return data
