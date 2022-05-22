import os
import re as regex
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitStatus:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'status'
    flags: list = []
    target: str = ''

    parser: Any

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '-s', 'name': '-short', 'argument': False, 'key_parameters': {'help': 'short git status, the default here'}},
        {'abbrev': '-l', 'name': '-long', 'argument': False, 'key_parameters': {'help': 'long git status, the default of the original command'}},
        {'abbrev': '-b', 'name': '-branch', 'argument': False, 'key_parameters': {'help': 'show the branch even on short mode'}},
        {'abbrev': '-a', 'name': '-all-untracked', 'argument': False, 'key_parameters': {'help': 'see all untracked files'}},
        {'abbrev': '-u', 'name': '-untracked', 'argument': False, 'key_parameters': {'help': 'see untracked files in the normal mode'}},
        {'abbrev': '-t', 'name': '-tracked', 'argument': False, 'key_parameters': {'help': 'see tracked files only'}},
        {'abbrev': '', 'name': 'partial_name', 'argument': None, 'key_parameters': {'help': 'partial name of the file or files to show'}},
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
            self.flags.append('--short')
            self.flags.append('--branch')
            return

        if options.s:
            self.flags.append('--short')
        elif options.l:
            self.flags.append('--long')

        if options.u:
            self.flags.append('--untracked-files=normal')
        elif options.t:
            self.flags.append('--untracked-files=no')
        elif options.a:
            self.flags.append('--untracked-files=all')

        if options.b:
            self.flags.append('--branch')

    def __map_command_value(self, options):
        if options.partial_name:
            self.target = self.__prepare_common_value(options.partial_name)

    def __prepare_common_value(self, original_value):
        filesList = ListResultsCaseIgnored()
        updated_value = filesList.find_changed_files_for_diff(original_value)

        if original_value == updated_value:
            updated_value = filesList.find_untracked_files_for_add(original_value)

        return self.__prepare_value_wildcards(updated_value)

    def __prepare_value_wildcards(self, value):
        target_value = ''
        if regex.search('\.\w?', value):
            target_value = '*{file_name}'.format(file_name=value)
        else:
            target_value = '*{file_name}*'.format(file_name=value)

        return target_value

    @staticmethod
    def go():
        BashGitStatus()
