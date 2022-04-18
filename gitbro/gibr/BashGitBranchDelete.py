import os

class BashGitBranchDelete:
    line: str = '{base} {action} {target}' # @todo - ":extras:"
    base: str = 'git'
    action: str = 'checkout -D'
    target: str = ''
    question: str = 'Are you sure you want to delete {target}? (Yy|Nn)'

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # @todo - colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        if not self.__confirm_just_in_case(values):
            return

        print(command)
        # os.system(command)

    def __confirm_just_in_case(self, values: list):
        answer = input(self.question.format(target=values[0]))
        if answer == 'y' or answer == 'Y':
            return True

        return False

    def __map_command(self, options: list = [], values: list = []):
        self.target = values[0]

        if (len(options) > 1 and options[1] == '-o'):
            self.action = 'push origin --delete'
            self.question = 'The branch {target} will be removed from the remote, are you sure? (Yy|Nn)'

        self.line = self.line.format(base=self.base, action=self.action, target=self.target)

        return self.line

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitBranchDelete(options, values)