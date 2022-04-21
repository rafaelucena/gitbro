import os
import re as regex

class BashGitDiffStat:
    line: str = '{base} {action} {target}' # @todo - ":extras:"
    base: str = 'git'
    action: str = 'diff --stat'
    target: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # @todo - colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        if len(values) > 0:
            self.target = self.__prepare_diff_value(values[0])

        self.line = self.line.format(base=self.base, action=self.action, target=self.target)

        return self.line

    def __prepare_diff_value(self, value):
        target_value = ''
        if regex.search('\.\w?', value):
            target_value = '*{file_name}'.format(file_name=value)
        else:
            target_value = '*{file_name}*'.format(file_name=value)

        return target_value

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitDiffStat(options, values)
