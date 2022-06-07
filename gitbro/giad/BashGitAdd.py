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
        {'abbrev': '', 'name': 'partial_file_name', 'argument': None, 'key_parameters': {'help': 'partial name of the file to add'}},
        {'abbrev': '-a', 'name': '-all', 'argument': False, 'key_parameters': {'help': 'add all files'}},
        {'abbrev': '-i', 'name': '-intent', 'argument': True, 'key_parameters': {'help': 'add files with --intent-to-add', 'metavar': 'partial_file_name', 'type': str}},
        {'abbrev': '-m', 'name': '-modified', 'argument': False, 'key_parameters': {'help': 'add only updated/tracked files'}},
        {'abbrev': '-n', 'name': '-new', 'argument': True, 'key_parameters': {'help': 'add new files', 'metavar': 'partial_file_name', 'type': str}},
        {'abbrev': '-u', 'name': '-update', 'argument': False, 'key_parameters': {'help': 'add only updated/tracked files'}},
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
        if options.a: #all
            self.flags.append('--all')
        elif options.m or options.u: #modified
            self.flags.append('-u')
        elif options.n: #new
            self.target = self.__prepare_untracked_file(options.n)
        elif options.i: #intent
            self.flags.append('--intent-to-add')
            self.target = self.__prepare_untracked_match(options.i)

    def __map_command_value(self, options):
        if not options.partial_file_name:
            return

        self.target = self.__prepare_common_diff_value(options.partial_file_name[0])

    def __prepare_common_diff_value(self, original_value):
        filesList = ListResultsCaseIgnored()
        updated_value = filesList.find_changed_files_for_diff(original_value)

        if original_value == updated_value:
            updated_value = filesList.find_untracked_files_for_add(original_value)

        return self.__prepare_value_wildcards(updated_value)

    def __prepare_untracked_file(self, original_value):
        filesList = ListResultsCaseIgnored()
        output_line = filesList.find_untracked_file_for_add(original_value)

        return output_line

    def __prepare_untracked_match(self, original_value):
        filesList = ListResultsCaseIgnored()
        updated_value = filesList.find_untracked_files_for_add(original_value)

        return self.__prepare_value_wildcards(updated_value)

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
