import os
import re as regex

class BashGitLogGrep:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'log'
    flags: list = []
    target: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        if len(values) == 0:
            print('Missing a value for this command')
            return

        command = self.__map_command(options, values)

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        self.__map_command_flags_by_common_usage(options)

        if '-g' in options or len(options) == 0:
            self.flags.append('-i --grep=\'{0}\''.format(values[0]))
        elif '-e' in options:
            self.flags.append('-i --grep=\'{0}\' --invert-grep'.format(values[0]))

        self.action = self.action.format(values[0])

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
        BashGitLogGrep(options, values)
