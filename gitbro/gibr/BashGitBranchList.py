import os

class BashGitBranchList:
    line: str = '{base} {action} {target}' # @todo - ":extras:"
    base: str = 'git'
    action: str = 'branch'
    target: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # @todo - colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        self.line = self.line.format(base=self.base, action=self.action, target=self.target)

        return self.line

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitBranchList(options, values)