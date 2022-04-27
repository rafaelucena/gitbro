import os

class BashGitStashBoom:
    line: str = '{base} {action} {target}' # @todo - ":extras:"
    base: str = 'git'
    action: str = 'stash clear'
    target: str = ''
    question: str = 'Are you sure you want to delete all {amount} stashes? (Yy|Nn)'

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # @todo - colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        if not self.__confirm_just_in_case():
            return

        print(command)
        # os.system(command)

    def __confirm_just_in_case(self):
        answer = input(self.question.format(amount=5))
        if answer == 'y' or answer == 'Y':
            return True

        return False

    def __map_command(self, options: list = [], values: list = []):
        self.line = self.line.format(base=self.base, action=self.action, target=self.target)

        return self.line

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitStashBoom(options, values)