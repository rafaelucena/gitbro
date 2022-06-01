import os
import re as regex

from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitLogCompare:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'log'
    flags: list = []
    target: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        self.__map_command_flags_by_common_usage(options)

        listResults = ListResultsCaseIgnored()

        compare_against = 'master'
        if (len(values) > 0):
            compare_against = listResults.find_branch_by_partial(values[0])

        self.flags.append('{0}..'.format(compare_against))

        if len(options) > 0 and regex.search(r'^-(\d+)', options[0]): #list
            self.target = options[0]
        else:
            self.target = ''

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_flags_by_common_usage(self, options: list):
        if '-p' in options: #pretty
            self.flags.append("--pretty=format:'%C(yellow)%h%Creset|%C(red)%ad%Creset|%C(yellow)%an%Creset:%s' --date=format:'%Y-%m-%d %H:%M:%S'")
        elif '-s' in options: #stat
            self.flags.append('--stat')
        elif '-d' in options: #diff
            self.flags.append('--patch-with-stat')
        elif '-o' in options: #oneline
            self.flags.append('--oneline')

        if '-n' in options: #no-merges
            self.flags.append('--no-merges')
        elif '-m' in options: #merges
            self.flags.append('--merges')

        if '-r' in options: #roadmap
            self.flags.append('--graph')

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitLogCompare(options, values)
