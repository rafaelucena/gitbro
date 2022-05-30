import os
import re as regex
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitBranch:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'branch'
    flags: list = []
    target: str = ''

    parser: Any

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '', 'name': 'branch_name', 'argument': None, 'key_parameters': {'help': 'name of the branch to checkout to'}},
        {'abbrev': '-b', 'name': '-branches', 'argument': False, 'key_parameters': {'help': 'list local branches'}},
        {'abbrev': '-n', 'name': '-new-branch', 'argument': True, 'key_parameters': {'help': 'checkout to a new branch', 'metavar': 'new_branch_name', 'type': str}},
        {'abbrev': '-r', 'name': '-remote-branches', 'argument': False, 'key_parameters': {'help': 'list remote branches'}},
    ]

    def __init__(self) -> None:
        self.parser = ArgumentsParser(self.options)
        command = self.__map_command(self.parser.get_mapped())

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        # os.system(command)

    def __map_command(self, options: list) -> str:
        self.__map_command_options(options)
        self.__map_command_value(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_options(self, options: list) -> None:
        if options.branch_name != False:
            return

        if self.parser.is_any_argument() == False:
            self.flags.append('-l')
            return

        if options.n: #new-branch
            self.action = 'checkout'
            self.flags.append('-b')
            self.target = options.n
            return

        if options.b: #branches
            self.flags.append('-l')

        if options.r: #remote-branches
            self.flags.append('-r')

    def __map_command_value(self, options):
        if options.branch_name:
            self.action = 'checkout'
            self.target = options.branch_name[0]

    @staticmethod
    def go():
        BashGitBranch()
