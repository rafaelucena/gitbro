import subprocess
import os
import re as regex

class BashGitDiffFile:
    line: str = '{base} {action} {target}' # @todo - ":extras:"
    base: str = 'git'
    action: str = 'diff'
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
        value = self.__prepare_case_insensitive_argument_search(value)

        target_value = ''
        if regex.search('\.\w?', value):
            target_value = '*{file_name}'.format(file_name=value)
        else:
            target_value = '*{file_name}*'.format(file_name=value)

        return target_value

    def __prepare_case_insensitive_argument_search(self, value):
        parsed_lines = {}
        mapped_needles = {}
        is_case_insensitive_argument_found = False

        changed_files = subprocess.getoutput('git diff --name-only')
        for changed_line in changed_files.splitlines():
            parsed_lines[changed_line] = changed_line.lower()

            tracked_argument_case_sensitive = changed_line.rfind(value)
            if tracked_argument_case_sensitive != -1:
                return value

            tracked_argument_case_insensitive = parsed_lines[changed_line].rfind(value)
            if tracked_argument_case_insensitive != -1:
                is_case_insensitive_argument_found = True

                needle_to_map = changed_line[tracked_argument_case_insensitive:tracked_argument_case_insensitive+len(value)]
                if needle_to_map in mapped_needles:
                    mapped_needles[needle_to_map] += 1
                else:
                    mapped_needles[needle_to_map] = 1

        if is_case_insensitive_argument_found == True:
            return next(iter(mapped_needles))

        return value

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitDiffFile(options, values)
