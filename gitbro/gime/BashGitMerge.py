import os
import re as regex
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitMerge:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'merge'
    flags: list = []
    target: str = ''

    parser: Any

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        # {'abbrev': '', 'name': 'partial_name', 'argument': None, 'key_parameters': {'help': 'partial name of the branch to merge'}},
        {'abbrev': '-a', 'name': '-abort', 'argument': False, 'key_parameters': {'help': 'abort the merge'}},
        {'abbrev': '-c', 'name': '-continue', 'argument': False, 'key_parameters': {'help': 'continue the merge'}},
        {'abbrev': '-q', 'name': '-quit', 'argument': False, 'key_parameters': {'help': 'quit the merge'}},
        # {'abbrev': '-s', 'name': '-short', 'argument': False, 'key_parameters': {'help': 'short git status, the default here'}},
        # {'abbrev': '-l', 'name': '-long', 'argument': False, 'key_parameters': {'help': 'long git status, the default of the original command'}},
        # {'abbrev': '-b', 'name': '-branch', 'argument': False, 'key_parameters': {'help': 'show the branch even on short mode'}},
        # {'abbrev': '-u', 'name': '-untracked', 'argument': False, 'key_parameters': {'help': 'see untracked files in the normal mode'}},
        # {'abbrev': '-t', 'name': '-tracked', 'argument': False, 'key_parameters': {'help': 'see tracked files only'}},
    ]

    def __init__(self) -> None:
        self.parser = ArgumentsParser(self.options)
        command = self.__map_command(self.parser.get_mapped())

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        # os.system(command)

    def __map_command(self, options: list) -> str:
        # self.__map_command_value(options)
        self.__map_command_options(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_options(self, options: list) -> None:
        if options.a: #abort
            self.target = '--abort'
        elif options.c: #continue
            self.target= '--continue'
        elif options.q: #quit
            self.target = '--quit'

    def __map_command_value(self, options):
        self.target = options.partial_name

    @staticmethod
    def go():
        BashGitMerge()
