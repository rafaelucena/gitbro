import os

from gitbro.abc.ListResultsCaseIgnored import ListResultsCaseIgnored

class BashGitMergeLast:
    line: str = '{base} {action} {flags} {target}' # TODO: ":extras:"
    base: str = 'git'
    action: str = 'merge'
    flags: list = []
    target: str = ''
    question: str = 'Are you sure you want to merge the branch ({branch}) into this one? (Yy|Nn)'

    def __init__(self, options: list = [], values: list = []) -> None:
        command = self.__map_command(options, values)

        if not self.__confirm_just_in_case():
            return

        # TODO: colorful print - print('{0} {1} {2}'.format('\033[32mgit', self.action, 'option'))
        print(command)
        os.system(command)

    def __map_command(self, options: list = [], values: list = []) -> str:
        self.__map_command_options(options, values)

        self.target = self.__prepare_last_branch_value()
        self.line = self.line.format(base=self.base, action=self.action, flags=' '.join(self.flags), target=self.target)

        return self.line

    def __confirm_just_in_case(self) -> bool:
        answer = input(self.question.format(branch=self.target))
        if answer == 'y' or answer == 'Y':
            return True

        return False

    def __map_command_options(self, options: list, values: list) -> None:
        if '-i' in options: #ignore (skip editing commit)
            self.flags.append('--no-edit')
        elif '-e' in options: #edit
            self.flags.append('--edit')

        if '-s' in options: #stat
            self.flags.append('--stat')
        elif '-q' in options: #quiet
            self.flags.append('--quiet')

        if '-d' in options: #dry-run
            self.flags.append('--no-commit')
            self.flags.append('--no-ff')

        if '-n' in options: #no-verify (skip git hooks)
            self.flags.append('--no-verify')

    def __prepare_last_branch_value(self) -> str:
        branchesList = ListResultsCaseIgnored()
        value = branchesList.find_last_branch_by_reflog()

        return value

    @staticmethod
    def go(options: list = [], values: list = []):
        BashGitMergeLast(options, values)
