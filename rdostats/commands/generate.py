import os
import arrow
import json
import logging
from cliff.command import Command

from rdostats.rdostats import RDOStats
from rdostats.compstats import component_graph
from rdostats.exc import *

LOG = logging.getLogger(__name__)

default_templates = ['index.html', 'report-grouped.html',
                     'report-ungrouped.html', 'report.txt']


class Generate(Command):
    def get_parser(self, prog_name):
        p = super(Generate, self).get_parser(prog_name)
        p.add_argument('--graph', '-g',
                       action='store_true',
                       help='Generate graph of no. of bugs by component')
        p.add_argument('--owners', '-o',
                       action='store_true',
                       help='Generate report by owner')
        p.add_argument('--latest', '-l',
                       action='store_true',
                       help='Update latest symlink to point to this report')
        p.add_argument('--template-dir', '-T',
                       help='Location of template files')
        p.add_argument('--template', '-t',
                        action='append',
                        help='Render a specific template')
        p.add_argument('--no-components', '-C',
                       action='store_false',
                       dest='components',
                       help='Generate per-component reports')
        p.add_argument('data', nargs='?')
        p.set_defaults(components=True)
        return p

    def take_action(self, args):
        basedir = self.app.config['basedir']

        if not args.template_dir:
            args.template_dir = self.app.config.get('template_dir')

        if args.data is None:
            date = arrow.now()
            args.data = os.path.join(basedir,
                                     date.format('YYYYMMDD'),
                                     'bugs.json')

        with open(args.data) as fd:
            data = json.load(fd)

        date = arrow.get(data['metadata']['date']).format('YYYYMMDD')
        workdir = os.path.join(basedir, date)
        if not os.path.isdir(workdir):
            os.makedirs(workdir)

        attributes = self.app.config.get('report_attributes', {})
        report = RDOStats(data,
                          template_dir=args.template_dir,
                          attributes=attributes)

        if args.graph:
            report.attributes['graph'] = component_graph(report,
                                                         max_comp_len=25)

        if args.template:
            templates = args.template
        else:
            templates = default_templates

        if args.owners:
            templates.append('report-people.html')

        for template in templates:
            with open(os.path.join(workdir, template), 'w') as fd:
                LOG.info('generating %s', fd.name)
                fd.write(report.render(template))

        if args.components:
            for comp in report.components():
                with open(os.path.join(
                        workdir, 'report-%s.html' % comp), 'w') as fd:
                    LOG.info('generating %s', fd.name)
                    fd.write(report.render('report-ungrouped.html',
                                           component=comp))

        if args.latest:
            latest = os.path.join(basedir, 'latest')
            if os.path.islink(latest):
                os.unlink(latest)
            os.symlink(date, latest)
