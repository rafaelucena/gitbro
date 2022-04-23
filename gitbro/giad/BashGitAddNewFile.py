import os
import re as regex

from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitAddNewFile:
    line: str = '{base} {action} {target}' # @todo - ":extras:"
    base: str = 'git'
    action: str = 'add {intent}'
    target: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # @todo - colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        if options[0] == '-i':
            self.action = self.action.format(intent='--intent-to-add')
            self.target = self.__prepare_untracked_match(values[0])
        else:
            self.action = self.action.format(intent='')
            self.target = self.__prepare_untracked_file(values[0])

        self.line = self.line.format(base=self.base, action=self.action, target=self.target)

        return self.line

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
        if regex.search('\.\w?', value):
            target_value = '*{file_name}'.format(file_name=value)
        else:
            target_value = '*{file_name}*'.format(file_name=value)

        return target_value

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitAddNewFile(options, values)
