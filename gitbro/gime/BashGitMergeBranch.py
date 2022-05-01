import subprocess
import os
import re as regex

from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitMergeBranch:
    line: str = '{base} {action} {flags} {target}' # @todo - ":extras:"
    base: str = 'git'
    action: str = 'merge'
    flags: str = ''
    target: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # @todo - colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        if len(values) > 0:
            self.__map_command_values(values)

        if len(options) > 0:
            self.__map_command_options(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=self.flags, target=self.target)

        return self.line

    def __map_command_options(self, options):
        if '-l' == options[0]:
            self.target = self.__prepare_last_branch_value()

        if '-n' in options:
            self.flags = '--no-verify'

    def __map_command_values(self, values):
        self.target = values[0]

    def __prepare_last_branch_value(self):
        filesList = ListResultsCaseIgnored()
        value = filesList.find_last_branch_by_reflog()

        return value

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitMergeBranch(options, values)
