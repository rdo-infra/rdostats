import jinja2
import arrow
import mistune
import logging
import textwrap

import defaults

LOG = logging.getLogger(__name__)


def filter_fill(value, width=75, **kwargs):
    return textwrap.fill(value, width=width, **kwargs)


def filter_format_date(value, format='YYYY-MM-DD'):
    return arrow.get(value).format(format)


def filter_humanize(value):
    now = arrow.utcnow()
    value = arrow.get(value)
    return value.humanize(now)


def filter_iter_count(value):
    return sum(1 for _ in value)


def filter_pluralize(value, singular, plural):
    if value == 1:
        label = singular
    else:
        label = plural

    return '%d %s' % (value, label)


def filter_markdown(value):
    return mistune.markdown(value)


def age_of(bug):
    now = arrow.utcnow()
    created = arrow.get(bug['creation_time'])
    return (now-created).days


def idle_of(bug):
    now = arrow.utcnow()
    last_changed = arrow.get(bug['last_change_time'])
    return (now-last_changed).days


def oldest_of(b1, b2):
    if b1 is None:
        return b2

    return min(b1, b2, key=lambda b: arrow.get(b['creation_time']))


class RDOStats (object):

    def __init__(self, current,
                 previous=None,
                 status_open=None,
                 status_fixed=None,
                 template_dir=None,
                 attributes=None):

        self.current = current
        self.previous = previous

        self.status_open = status_open or defaults.status_open
        self.status_fixed = status_fixed or defaults.status_fixed
        self.template_dir = template_dir or defaults.template_dir
        self.attributes = attributes

        self.setup_templates()
        self.process_data()

    def setup_templates(self):
        self.env = jinja2.Environment(
            loader=jinja2.loaders.FileSystemLoader(self.template_dir),
        )
        self.env.filters['format_date'] = filter_format_date
        self.env.filters['humanize'] = filter_humanize
        self.env.filters['iter_count'] = filter_iter_count
        self.env.filters['pluralize'] = filter_pluralize
        self.env.filters['markdown'] = filter_markdown
        self.env.filters['fill'] = filter_fill

    def process_data(self):
        self.metadata = self.current['metadata']
        self.date = arrow.get(self.current['metadata']['date'])
        self.people = self.people_stats()

    def people_stats(self):
        counter = {}
        for bug in self.bugs(status=self.status_open):
            owner = bug['assigned_to']
            if owner not in counter:
                counter[owner] = {
                    'name': owner,
                    'bugs': 0,
                    'avg_age': 0,
                    'avg_idle': 0,
                    'oldest': None,
                }

            x = counter[owner]
            x['bugs'] += 1
            x['avg_age'] = (
                (x['avg_age'] + age_of(bug))/x['bugs'])
            x['avg_idle'] += idle_of(bug)
            x['oldest'] = oldest_of(x['oldest'], bug)

        return counter


    def render(self, template_name, **kwargs):
        template = self.env.get_template(template_name)
        return template.render(report=self, **kwargs).encode('utf8')

    def bugs(self, component=None, status=None):
        return (bug for bug in self.current['bugs']
                if (not component or bug['component'] == component)
                and (not status or bug['status'] in status))

    def components(self, status=None):
        return set(bug['component'] for bug in self.current['bugs']
                   if (status is None or bug['status'] in status))
