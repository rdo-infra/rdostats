import os

import arrow
import json
import xmlrpclib
from cliff.command import Command

from rdostats.rdostats import RDOStats
from rdostats.fetch import fetch_bugs


def json_default(obj):
    '''This allows us to serialize xmlrpclib.DateTime
    objects (which is what Bugzilla gives us for dates).'''
    if isinstance(obj, xmlrpclib.DateTime):
        return str(arrow.get(obj.timetuple()))
    elif isinstance(obj, arrow.arrow.Arrow):
        return str(obj)

    raise TypeError(repr(obj) + " is not JSON serializable")


class Fetch(Command):

    def take_action(self, args):
        date = arrow.now().format('YYYYMMDD')
        data = fetch_bugs(
            url = self.app.config['bugzilla']['url'],
            product = self.app.config['bugzilla']['product'],
            )

        workdir = os.path.join(self.app.config['basedir'], date)
        if not os.path.isdir(workdir):
            os.makedirs(workdir)
        datafile = os.path.join(workdir, 'bugs.json')
        with open(datafile, 'w') as fd:
            json.dump(data, fd, indent=2, default=json_default)

        print datafile
