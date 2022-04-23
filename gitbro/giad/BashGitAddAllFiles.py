import os

from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitAddAllFiles:
    line: str = '{base} {action} {target}' # @todo - ":extras:"
    base: str = 'git'
    action: str = 'add --all'
    target: str = ''
    question: str = 'All the files listed will be added, including untracked, are you sure? (Yy|Nn)'

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # @todo - colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        if not self.__confirm_just_in_case():
            return

        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        self.line = self.line.format(base=self.base, action=self.action, target=self.target)

        return self.line

    def __confirm_just_in_case(self):
        answer = input(self.question)
        if answer == 'y' or answer == 'Y':
            return True

        return False

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitAddAllFiles(options, values)
