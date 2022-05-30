import os
import re as regex
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitDiff:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'diff'
    flags: list = []
    target: str = ''

    parser: Any

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '-a', 'name': '-all', 'argument': False, 'key_parameters': {'help': 'see all the changes'}},
        {'abbrev': '-q', 'name': '-queued', 'argument': False, 'key_parameters': {'help': 'see all the queued changes'}},
        {'abbrev': '-s', 'name': '-stat', 'argument': False, 'key_parameters': {'help': 'see the changes as --stat'}},
    ]

    def __init__(self) -> None:
        self.parser = ArgumentsParser(self.options)
        command = self.__map_command(self.parser.get_mapped())

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list) -> str:
        self.__map_command_options(options)
        self.__map_command_value(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_options(self, options: list) -> None:
        if self.parser.is_any_argument() == False:
            return

        if options.a: #all
            pass

        if options.q: #cached
            self.flags.append('--cached')

        if options.s: #stat
            self.flags.append('--stat')

    def __map_command_value(self, options):
        pass

    @staticmethod
    def go():
        BashGitDiff()
