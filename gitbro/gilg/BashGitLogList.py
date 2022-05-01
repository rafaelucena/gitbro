import os
import re as regex

class BashGitLogList:
    line: str = '{base} {action} {format} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'log {grep}'
    format: str = ''
    target: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        if ('-g' in options or len(options) == 0) and len(values) > 0: #grep
            self.action = self.action.format(grep='-i --grep={0}'.format(values[0]))
        elif '-e' in options and len(values) > 0: #exclude
            self.action = self.action.format(grep='-i --grep={0} --invert-grep'.format(values[0]))
        elif '-c' in options and len(values) > 0: #compare
            self.action = self.action.format(grep='{0}..'.format(values[0]))
        else:
            self.action = self.action.format(grep='')

        if '-p' in options: #pretty
            self.format = "--pretty=format:'%C(yellow)%h%Creset|%C(red)%ad%Creset|%C(yellow)%an%Creset:%s' --date=format:'%Y-%m-%d %H:%M:%S'"
        elif '-t' in options: #traces
            self.format = '--graph'
        elif '-d' in options: #diff
            self.format = '--patch-with-stat'
        elif '-o' in options: #oneline
            self.format = '--oneline'

        if len(options) > 0 and regex.search('^-(\d+)', options[0]): #list
            self.target = options[0]
        else:
            self.target = ''

        self.line = self.line.format(base=self.base, action=self.action, target=self.target, format=self.format)

        return self.line

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitLogList(options, values)
