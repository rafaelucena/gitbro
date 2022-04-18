import os

class BashGitBranchKill:
    line: str = '{base} {action} {target}' # @todo - ":extras:"
    base: str = 'git'
    action: str = 'push origin --delete'
    target: str = ''
    question: str = 'The branch {target} will be removed from the remote, are you sure? (Yy|Nn)'

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
        self.line = self.line.format(base=self.base, action=self.action, target=self.target)

        return self.line

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitBranchKill(options, values)