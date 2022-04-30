import os

class BashGitStashList:
    line: str = '{base} {action} {pretty} {target}' # TODO: - ":extras:"
    base: str = 'git'
    action: str = 'stash list'
    pretty: str = '--pretty=format:"%gd: %<(70,trunc)%s: %C(green)(%cr)%C(reset)"'
    target: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # TODO: - colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        if (len(options) <= 0 or options[0] != '-l'):
            self.pretty = ''

        self.line = self.line.format(base=self.base, action=self.action, pretty=self.pretty, target=self.target)

        return self.line

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitStashList(options, values)
