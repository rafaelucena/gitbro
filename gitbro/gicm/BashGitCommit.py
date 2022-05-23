import os
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser

class BashGitCommit:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'commit'
    flags: list = []
    target: str = ''

    parser: Any

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '-m', 'name': '-message', 'argument': True, 'key_parameters': {'help': 'message for the commit', 'action': 'extend', 'metavar': 'commit_message', 'nargs': '+', 'type': str}},
        {'abbrev': '-n', 'name': '-no-verify', 'argument': False, 'key_parameters': {'help': 'ignore git hooks'}},
        {'abbrev': '', 'name': 'commit_message', 'argument': None, 'key_parameters': {'help': 'message for the commit', 'type': str}},
    ]

    def __init__(self) -> None:
        self.parser = ArgumentsParser(self.options)
        command = self.__map_command(self.parser.get_mapped())

        # print(self.parser.get_mapped())
        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list) -> str:
        self.__map_command_options(options)
        self.__map_command_value(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_options(self, options: list) -> None:
        # if self.parser.is_any_argument() == False:
        #     self.flags.append('--short')
        #     self.flags.append('--branch')
        #     return

        if options.m:
            self.target = '-m \'' + ' '.join(options.m) + '\''

        if options.n:
            self.flags.append('--no-verify')

    def __map_command_value(self, options):
        if options.commit_message:
            self.target = '-m \'' + ' '.join(options.commit_message) + '\''

    @staticmethod
    def go():
        BashGitCommit()
