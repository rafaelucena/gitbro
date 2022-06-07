import os
import re as regex
from typing import Any
from gitbro.abc.ArgumentsParser import ArgumentsParser
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitAdd:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'add'
    flags: list = []
    target: str = ''

    parser: Any

    # TODO: implement exclusive group on arguments parsing
    options: list = [
        {'abbrev': '', 'name': 'partial_file_name', 'argument': None, 'key_parameters': {'help': 'partial name of the file to diff'}},
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
        pass

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
        BashGitAdd()
