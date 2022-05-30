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
        {'abbrev': '', 'name': 'partial_file_name', 'argument': None, 'key_parameters': {'help': 'partial name of the file to diff'}},
        {'abbrev': '-a', 'name': '-all', 'argument': False, 'key_parameters': {'help': 'see all the changes, including staged'}},
        {'abbrev': '-d', 'name': '-diff', 'argument': False, 'key_parameters': {'help': 'see the changes with the --patch format'}},
        {'abbrev': '-q', 'name': '-queued', 'argument': False, 'key_parameters': {'help': 'see all the queued changes'}},
        {'abbrev': '-s', 'name': '-stat', 'argument': False, 'key_parameters': {'help': 'see the changes as --stat'}},
        {'abbrev': '-i', 'name': '-ignore-queued', 'argument': False, 'key_parameters': {'help': 'see the changes as --stat'}},
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
            self.flags.append('--stat')
            return

        if options.a: #all
            self.flags.append('HEAD')

        if options.d: #diff
            self.flags.append('--patch-with-stat')
        elif options.s: #stat
            self.flags.append('--stat')

        if options.q: #queued|staged
            self.flags.append('--staged')

    def __map_command_value(self, options):
        if not options.partial_file_name:
            return

        self.target = self.__prepare_common_diff_value(options.partial_file_name[0])

        if options.a: #all
            self.target = self.__prepare_common_diff_value(options.partial_file_name[0])
        elif options.q: #queued|staged
            self.target = self.__prepare_queued_diff_value(options.partial_file_name[0])

    def __prepare_common_diff_value(self, value):
        filesList = ListResultsCaseIgnored()
        value = filesList.find_changed_files_for_diff(value)

        return self.__prepare_value_wildcards(value)

    def __prepare_queued_diff_value(self, value):
        filesList = ListResultsCaseIgnored()
        value = filesList.find_queued_files_for_diff(value)

        return self.__prepare_value_wildcards(value)

    def __prepare_value_wildcards(self, value):
        target_value = ''
        if regex.search(r'\.\w?$', value):
            target_value = '*{file_name}'.format(file_name=value)
        else:
            target_value = '*{file_name}*'.format(file_name=value)

        return target_value

    @staticmethod
    def go():
        BashGitDiff()
