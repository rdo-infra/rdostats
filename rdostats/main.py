import sys
import yaml

from cliff.app import App
from cliff.commandmanager import CommandManager


class RDOStats(App):
    def __init__(self):
        super(RDOStats, self).__init__(
            description='RDO bugzilla statistics',
            version='1',
            command_manager=CommandManager('rdostats'),
        )

    def build_option_parser(self, *args, **kwargs):
        parser = super(RDOStats, self).build_option_parser(*args, **kwargs)

        parser.add_argument('--config', '-f',
                            default='rdostats.yaml')

        return parser

    def initialize_app(self, args):
        with open(self.options.config) as fd:
            self.config = yaml.load(fd)


app = RDOStats()


def main():
    app.run(sys.argv[1:])


if __name__ == '__main__':
    main()
