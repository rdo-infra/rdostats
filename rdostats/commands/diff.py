import os
import arrow
import json
import logging
from cliff.command import Command

from rdostats.rdostats import RDOStats
from rdostats.fetch import update_bugs
from rdostats.compstats import component_graph
from rdostats.exc import *

LOG = logging.getLogger(__name__)

default_templates = ['index.html', 'report-grouped.html',
                     'report-ungrouped.html', 'report.txt']


class Diff(Command):
    def get_parser(self, prog_name):
        p = super(Diff, self).get_parser(prog_name)
        p.add_argument('--template-dir', '-T',
                       help='Location of template files')
        p.add_argument('--template', '-t',
                        action='append',
                        help='Render a specific template')
        p.add_argument('data')
        p.set_defaults(components=True)
        return p

    def take_action(self, args):
        basedir = self.app.config['basedir']

        if not args.template_dir:
            args.template_dir = self.app.config.get('template_dir')

        with open(args.data) as fd:
            data = json.load(fd)

        update_bugs(data)
        report = RDOStats(data, template_dir=args.template_dir)
        print report.render('report-changed.html')
