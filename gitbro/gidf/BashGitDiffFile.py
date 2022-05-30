import subprocess
import os
import re as regex

from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitDiffFile:
    line: str = '{base} {action} {flags} {target}' # @todo - ":extras:"
    base: str = 'git'
    action: str = 'diff'
    flags: list = []
    target: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # @todo - colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []) -> str:
        if len(options) > 0:
            self.__map_command_options(options, values)

        if len(values) > 0:
            self.__map_command_values(options, values)

        if (len(options) == 0 and len(values) == 0):
            self.flags.append('HEAD')
            self.flags.append('--stat')

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_values(self, options: list, values: list) -> None:
        self.target = self.__prepare_common_diff_value(values[0])

        if len(options) > 0:
            if '-a' in options: #all
                self.target = self.__prepare_common_diff_value(values[0])
            elif '-q' in options: #queued
                self.target = self.__prepare_queued_diff_value(values[0])

    def __map_command_options(self, options: list, values: list):
        if '-a' in options: #all
            self.flags = []
        elif '-q' in options: #queued
            self.flags.append('--cached')

        if '-s' in options: #stat
            self.flags.append('--stat')

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
    def go(options: list = [], values: list = []):
        BashGitDiffFile(options, values)
