import os

from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitMergeActions:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'merge'
    flags: list = []
    target: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        # os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        if len(options) > 0:
            self.__map_command_options(options)

        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __map_command_options(self, options):
        if '-a' in options: #abort
            self.target = '--abort'
        elif '-c' in options: #continue
            self.target= '--continue'
        elif '-q' in options: #quit
            self.target = '--quit'

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitMergeActions(options, values)
