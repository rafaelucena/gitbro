import os
from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitStash:
    line: str = '{base} {action} {target} {comment}' # TODO: ":extras:"
    base: str = 'git'
    action: str = ''
    target: str = 'stash@{{{index}}}'
    question: str = ''
    comment: str = ''

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        if not self.__confirm_just_in_case():
            return

        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []):
        self.target = self.__map_command_target(values)
        self.line = self.line.format(base=self.base, action=self.action, target=self.target, comment=self.comment)

        return self.line

    def __map_command_target(self, values):
        if len(values) > 0:
            self.target = self.target.format(index=values[0])

        return self.target

    def __confirm_just_in_case(self):
        self.question = self.__map_question_confirmation()
        if (self.question == ''):
            return True

        answer = input(self.question)
        if answer == 'y' or answer == 'Y':
            return True

        return False

    def __map_question_confirmation()

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitStash(options, values)
