import os

class BashGitLogList:
    line: str = '{base} {action} {target} {format}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'log'
    format: str = ''
    target: str = '-{results}'

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        if (len(options) > 0 and options[0] == '-p') or (len(options) > 1 and options[1] == '-p'):
            self.format = "--pretty=format:'%C(yellow)%h%Creset|%C(red)%ad%Creset|%C(yellow)%an%Creset:%s' --date=format:'%Y-%m-%d %H:%M:%S'"

        if len(values) > 0:
            self.target = self.target.format(results=values[0])
        else:
            self.target = ''

        self.line = self.line.format(base=self.base, action=self.action, target=self.target, format=self.format)

        return self.line

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitLogList(options, values)
